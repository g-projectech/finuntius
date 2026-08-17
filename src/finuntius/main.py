import argparse
import sys
from importlib.metadata import version, PackageNotFoundError
from pathlib import Path
from rich.console import Console
from finuntius.config import retrieve_api_key, get_preferred_language, interactively_select_language
from finuntius.finnhub_fetcher import fetch_financial_news
from finuntius.formatter import display_news_table
from finuntius.exporter import format_as_json, format_as_markdown, save_content_to_file
from finuntius.translations import t

console = Console()
err_console = Console(stderr=True)

VALID_OUTPUT_EXTENSIONS = (".json", ".md", ".markdown")
MAX_DAYS_LOOKBACK = 365

try:
    __version__ = version("finuntius")
except PackageNotFoundError:
    __version__ = "1.0.0"

def main():
    selected_language = get_preferred_language()

    #inizializza gestore argomenti da CLI
    parser = argparse.ArgumentParser(
        prog="finuntius",
        description=t("cli_desc", selected_language),
        epilog=t("cli_epilog", selected_language),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False
    )

    parser._positionals.title = t("group_positional", selected_language)

    parser.add_argument(
        "query",
        type=str,
        nargs="?",
        default=None,
        metavar="QUERY",
        help=t("cli_help_query", selected_language)
    )

    # gruppo 1 - info generali e di config
    general_group = parser.add_argument_group(t("group_general", selected_language))
    
    general_group.add_argument(
        "-h", "--help",
        action="help",
        default=argparse.SUPPRESS,
        help=t("cli_help_h", selected_language)
    )
    general_group.add_argument(
        "-v", "--version",
        action="version",
        version=f"finuntius {__version__}",
        help=t("cli_help_v", selected_language)
    )
    general_group.add_argument(
        "-c", "--set-language",
        action="store_true",
        dest="set_language",
        help=t("cli_help_c", selected_language)
    )
    general_group.add_argument(
        "-k", "--api-key",
        type=str,
        default=None,
        metavar="KEY",
        help=t("cli_help_k", selected_language)
    )

    # gruppo 2 - filtri per la ricerca
    search_parameters = parser.add_argument_group(t("search_parameters", selected_language))

    search_parameters.add_argument(
        "-l", "--limit",
        type=int,
        default=5,
        metavar="LIMIT",
        help=t("cli_help_l", selected_language)
    )
    search_parameters.add_argument(
        "-d", "--days",
        type=int,
        default=7,
        metavar="DAYS",
        help=t("cli_help_d", selected_language)
    )

    # gruppo 3 - output e salvatggio
    output_group = parser.add_argument_group(t("output_group", selected_language))

    output_group.add_argument(
        "-j", "--json",
        action="store_true",
        help=t("cli_help_j", selected_language)
    )
    output_group.add_argument(
        "-m", "--markdown",
        action="store_true",
        dest="markdown",
        help=t("cli_help_m", selected_language)
    )
    output_group.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        metavar="FILE",
        help=t("cli_help_o", selected_language)
    )

    parsed_arguments = parser.parse_args()

    # se è richiesta config lingua la chiede senza query
    if parsed_arguments.set_language:
        interactively_select_language()
        return

    #verifica presenza ticker o isin
    if not parsed_arguments.query:
        parser.error(t("cli_req_query", selected_language))

    # se -j e -m sono attivi mostra errore
    if parsed_arguments.json and parsed_arguments.markdown:
        err_console.print(f"[bold red]{t('error_prefix', selected_language)}[/bold red] {t('cli_conflicting_format', selected_language)}")
        sys.exit(1)

    #limiti per news e giorni
    if parsed_arguments.limit <= 0:
        err_console.print(f"[bold red]{t('error_prefix', selected_language)}[/bold red] {t('cli_invalid_limit', selected_language, value=parsed_arguments.limit)}")
        sys.exit(1)

    if parsed_arguments.days <= 0:
        err_console.print(f"[bold red]{t('error_prefix', selected_language)}[/bold red] {t('cli_invalid_days', selected_language, value=parsed_arguments.days)}")
        sys.exit(1)

    if parsed_arguments.days > MAX_DAYS_LOOKBACK:
        err_console.print(f"[bold red]{t('error_prefix', selected_language)}[/bold red] {t('cli_days_too_large', selected_language, value=parsed_arguments.days, max=MAX_DAYS_LOOKBACK)}")
        sys.exit(1)

    #flag di output iniziali
    is_json_output = parsed_arguments.json
    is_markdown_output = parsed_arguments.markdown

    #gestione e validazione del file di salvataggio
    if parsed_arguments.output:
        output_file_path = Path(parsed_arguments.output)
        file_extension = output_file_path.suffix.lower()

        #se manca estensione la aggiunge, else verifica che sia JSON
        if parsed_arguments.json:
            if file_extension == "":
                parsed_arguments.output = str(output_file_path.with_suffix(".json"))
            elif file_extension != ".json":
                err_console.print(f"[bold red]{t('error_prefix', selected_language)}[/bold red] {t('cli_ext_mismatch_json', selected_language, ext=file_extension)}")
                sys.exit(1)

        #se manca estensione la aggiunge, else verifica che sia MD
        elif parsed_arguments.markdown:
            if file_extension == "":
                parsed_arguments.output = str(output_file_path.with_suffix(".md"))
            elif file_extension not in (".md", ".markdown"):
                err_console.print(f"[bold red]{t('error_prefix', selected_language)}[/bold red] {t('cli_ext_mismatch_md', selected_language, ext=file_extension)}")
                sys.exit(1)

        # se non sono stati passati ne -j ne -m, verifica che estensione del file sia supportata
        elif file_extension not in VALID_OUTPUT_EXTENSIONS:
            err_console.print(f"[bold red]{t('error_prefix', selected_language)}[/bold red] {t('unsupported_output_format', selected_language)}")
            sys.exit(1)

        #deduce autoamticamente formato di esportazione dall'estensione
        else:
            is_json_output = file_extension == ".json"
            is_markdown_output = file_extension in (".md", ".markdown")

    try:
        #recupero API key
        api_token = retrieve_api_key(parsed_arguments.api_key, selected_language)

        #recupero news da finhub
        with err_console.status(f"[bold cyan]{t('fetching_news', selected_language, query=parsed_arguments.query)}[/bold cyan]", spinner="dots"):
            news_data = fetch_financial_news(
                symbol=parsed_arguments.query,
                max_items=parsed_arguments.limit,
                api_key=api_token,
                days_back=parsed_arguments.days,
                lang=selected_language
            )

        #output formato JSON
        if is_json_output:
            output_content = format_as_json(parsed_arguments.query, news_data)
            if parsed_arguments.output:
                save_content_to_file(output_content, parsed_arguments.output, selected_language)
            else:
                print(output_content)

        #output formato JSON
        elif is_markdown_output:
            output_content = format_as_markdown(parsed_arguments.query, news_data, selected_language)
            if parsed_arguments.output:
                save_content_to_file(output_content, parsed_arguments.output, selected_language)
            else:
                print(output_content)

        #mostra tabella a schermo
        else:
            display_news_table(parsed_arguments.query, news_data, selected_language)

    #gestione errori
    except Exception as error:
        err_console.print(f"[bold red]{t('error_prefix', selected_language)}[/bold red] {error}")
        sys.exit(1)

if __name__ == "__main__":
    main()
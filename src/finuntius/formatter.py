from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from typing import List, Dict
from finuntius.translations import t, DEFAULT_LANGUAGE

console = Console()

# crea e stampa il pannello superiore alla tabella che contiene le news
def render_title(target: str, total_results: int, lang: str = DEFAULT_LANGUAGE) -> None:
    title_text = Text()
    title_text.append(" FINUNTIUS ", style="bold black on cyan")
    title_text.append(f" \u2502 {t('panel_subtitle', lang)}\n", style="bold white")
    title_text.append(f" {t('panel_target_label', lang)} ", style="dim")
    title_text.append(f"{target.upper()} ", style="bold yellow")
    title_text.append(f"\u2502 {t('panel_results_label', lang)} ", style="dim")
    title_text.append(f"{total_results}", style="bold green")

    console.print(
        Panel(
            title_text,
            box=box.ROUNDED,
            border_style="cyan",
            expand=True
        )
    )

# stampa, se non ci sono news avviso in un pannello, else la tabella con le news
def display_news_table(target: str, articles_array: List[Dict[str, str]], lang: str = DEFAULT_LANGUAGE) -> None:
    if not articles_array:
        console.print(
            Panel(
                f"[bold red]{t('no_news_found', lang)}[/bold red] [cyan]{target}[/cyan]\n"
                f"[dim]{t('coverage_hint', lang)}[/dim]",
                box=box.ROUNDED,
                border_style="red"
            )
        )
        return

    render_title(target, len(articles_array), lang)

    table = Table(
        box=box.ROUNDED,
        header_style="bold magenta",
        border_style="blue",
        show_lines=True,
        expand=True
    )

    table.add_column(t("table_header_num", lang), style="bold dim cyan", width=3, justify="center")
    table.add_column(t("table_header_headline", lang), style="bold white", ratio=4)
    table.add_column(t("table_header_source", lang), style="bold yellow", ratio=2)
    table.add_column(t("table_header_date", lang), style="dim green", ratio=2)
    table.add_column(t("table_header_url", lang), style="underline blue", ratio=3)

    for idx, item in enumerate(articles_array, start=1):
        table.add_row(
            str(idx),
            item["title"],
            item["source"],
            item["date"],
            item["link"]
        )

    console.print(table) #stampa la table
import os
import stat
from pathlib import Path
from dotenv import dotenv_values, load_dotenv
from rich.console import Console
from rich.prompt import Prompt
from finuntius.translations import t, DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES

console = Console()

load_dotenv()

# configurazione directory base
xdg_config_home = os.getenv("XDG_CONFIG_HOME")
CONFIG_DIR = Path(xdg_config_home) / "finuntius" if xdg_config_home else Path.home() / ".config" / "finuntius"

CONFIG_FILE = CONFIG_DIR / ".env"

# prende la lingua per configurare le stampe. La cerca nell' .env, altrimenti nel configuration file, altrimenti restituisce valore default
def get_preferred_language() -> str:
    env_lang = os.getenv("FINUNTIUS_LANG")
    if env_lang in SUPPORTED_LANGUAGES:
        return env_lang

    if CONFIG_FILE.exists():
        user_config = dotenv_values(CONFIG_FILE)
        saved_lang = user_config.get("FINUNTIUS_LANG")
        if saved_lang in SUPPORTED_LANGUAGES:
            return saved_lang

    return DEFAULT_LANGUAGE

#prende le API key. Segue una "cascata" per prenderle, cerca prima tramite comando CLI, else nell'.env locale, altrimenti nel configuration file globale, altrimenti lo chiede nelle CLI e lo salva nel config file globale
def retrieve_api_key(cli_key: str = None, lang: str = DEFAULT_LANGUAGE) -> str:
    if cli_key:
        return cli_key

    env_key = os.getenv("FINNHUB_API_KEY")
    if env_key:
        return env_key

    if CONFIG_FILE.exists():
        user_config = dotenv_values(CONFIG_FILE)
        saved_key = user_config.get("FINNHUB_API_KEY")
        if saved_key:
            return saved_key

    console.print(f"\n[bold yellow]{t('api_key_missing', lang)}[/bold yellow]")
    console.print(t("api_key_intro", lang))
    console.print(f"{t('api_key_get_it', lang)} [bold cyan link=https://finnhub.io/]https://finnhub.io/[/bold cyan link]")
    console.print(f"[dim italic]{t('disclaimer', lang)}[/dim italic]\n")

    new_key = Prompt.ask(f"[bold cyan]{t('prompt_api_key', lang)}[/bold cyan]", password=True).strip()

    if not new_key:
        raise ValueError(t("api_key_empty_error", lang))

    store_api_key(new_key, lang)
    return new_key

# aggiorna i valori del file di configuraz. e li unifica con quelli vecchi. Vengono applicati anche permessi restrittivi (chmod 600)
def update_config_values(updates: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    existing = dict(dotenv_values(CONFIG_FILE)) if CONFIG_FILE.exists() else {}
    existing.update(updates)

    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    mode = stat.S_IRUSR | stat.S_IWUSR
    fd = os.open(CONFIG_FILE, flags, mode)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        for key, value in existing.items():
            f.write(f"{key}={value}\n")

# salva le API key nel file config globale
def store_api_key(api_key: str, lang: str = DEFAULT_LANGUAGE) -> None:
    update_config_values({"FINNHUB_API_KEY": api_key})
    console.print(f"[bold green]{t('api_key_saved', lang)}[/bold green] [dim]{CONFIG_FILE}[/dim]\n")

# salva lingua scelta nel file config globale
def store_language(lang: str) -> None:
    if lang not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {lang}")
    update_config_values({"FINUNTIUS_LANG": lang})
    console.print(f"\n[bold green]{t('language_saved', lang)}[/bold green] {lang}\n")

# chiede all'utente che lingua scegliere
def interactively_select_language() -> str:
    current_lang = get_preferred_language()
    
    console.print(f"\n[bold cyan]{t('language_selection_title', current_lang)}[/bold cyan]")
    console.print(f"  [bold]1[/bold]) {t('language_option_english', current_lang)}")
    console.print(f"  [bold]2[/bold]) {t('language_option_italian', current_lang)}\n")

    prompt_text = t('language_prompt_label', current_lang)
    
    choice = Prompt.ask(
        prompt_text, 
        choices=["1", "2"], 
        default="1", 
        show_choices=False, 
        show_default=False
    )
    
    lang = "en" if choice == "1" else "it"

    if lang == current_lang:
        console.print(f"\n[bold yellow]{t('language_already_set', current_lang)}[/bold yellow] {lang}\n")
        return lang

    store_language(lang)
    return lang
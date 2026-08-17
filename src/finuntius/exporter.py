import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict
from rich.console import Console
from finuntius.translations import t, DEFAULT_LANGUAGE

console = Console()

# prende i dati e li converte in str JSON (li mantiene in memoria)
def format_as_json(target: str, articles_array: List[Dict[str, str]]) -> str:
    data = {
        "target": target.upper(),
        "total_results": len(articles_array),
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "news": articles_array
    }
    return json.dumps(data, indent=2, ensure_ascii=False)

# prende i dati e li converte in str MD
def format_as_markdown(target: str, articles_array: List[Dict[str, str]], lang: str = DEFAULT_LANGUAGE) -> str:
    lines = [
        f"# {t('export_title', lang, target=target.upper())}",
        f"**{t('export_fetched_at', lang)}** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC  ",
        f"**{t('export_total_results', lang)}** {len(articles_array)}\n",
        "---"
    ]

    if not articles_array:
        lines.append(f"\n*{t('export_no_news', lang, target=target.upper())}*")
        lines.append(f"\n_{t('coverage_hint', lang)}_")
        return "\n".join(lines)

    for idx, item in enumerate(articles_array, start=1):
        lines.append(f"\n### {idx}. {item.get('title', 'N/A')}")
        lines.append(f"- **{t('export_source', lang)}** {item.get('source', 'Unknown')}")
        lines.append(f"- **{t('export_date', lang)}** {item.get('date', 'N/A')}")
        lines.append(f"- **{t('export_url', lang)}** {item.get('link', 'N/A')}")

        summary = item.get("summary", "").strip()
        if summary:
            lines.append(f"- **{t('export_summary', lang)}** {summary}")

        lines.append("\n---")

    return "\n".join(lines)

#prende il txt formattato in JSON o MD e lo inserisce in un file che verrà salvato su disco
def save_content_to_file(content: str, filepath: str, lang: str = DEFAULT_LANGUAGE) -> None:
    target_path = Path(filepath)
    if target_path.parent != Path(""):
        target_path.parent.mkdir(parents=True, exist_ok=True)

    with open(target_path, "w", encoding="utf-8") as file_handle:
        file_handle.write(content)
    console.print(f"[bold green]{t('output_saved', lang)}[/bold green] [cyan]{filepath}[/cyan]")
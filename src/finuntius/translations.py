DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = ("en", "it")

TRANSLATIONS = {
    "en": {
        # config.py -API
        "api_key_missing": "Finnhub API Key not found.",
        "api_key_intro": "To use Finuntius, a Finnhub API key is required (the free plan is sufficient).",
        "api_key_get_it": "Get your free API key by creating an account at:",
        "disclaimer": "* Disclaimer: Finuntius is an independent open-source project and is not affiliated, endorsed, or sponsored by Finnhub.",
        "prompt_api_key": "Enter your Finnhub API Key",
        "api_key_empty_error": "API Key cannot be empty.",
        "api_key_saved": "API Key saved successfully to:",

        #config.py
        "language_saved": "Language set to:",
        "language_already_set": "Language currently in use on Finuntius:",
        "language_option_english": "English",
        "language_option_italian": "Italiano",
        "language_prompt_label": "Enter choice",
        "language_selection_title": "Select your language",

        # formatter.py
        "panel_subtitle": "Financial News Terminal (Data via Finnhub API)",
        "panel_target_label": "Target:",
        "panel_results_label": "Results Found:",
        "no_news_found": "No financial news found for target:",
        "table_header_num": "#",
        "table_header_headline": "Headline",
        "table_header_source": "Source",
        "table_header_date": "Date (UTC)",
        "table_header_url": "URL",

        # exporteer.py
        "export_title": "Financial News for {target}",
        "export_fetched_at": "Fetched at:",
        "export_total_results": "Total Results:",
        "export_source": "Source:",
        "export_date": "Date (UTC):",
        "export_url": "URL:",
        "export_summary": "Summary:",
        "export_no_news": "No financial news found for {target}.",
        "output_saved": "Output saved successfully to:",

        # finnhub_fetcher.py
        "missing_api_key": "Missing API Key. Set 'FINNHUB_API_KEY' environment variable or pass it via '--api-key'.",
        "invalid_api_key": "Invalid or expired Finnhub API Key.",
        "rate_limit": "Finnhub rate limit reached. Check the request limits for your plan on the Finnhub dashboard (all plans share a 30 requests/second cap).",
        "unexpected_response": "Unexpected API response: {data}",
        "network_error": "Network error while connecting to Finnhub: {err}",
        "isin_not_found": "No company found for ISIN '{isin}'.",
        "premium_ticker_required": "This ticker requires a paid Finnhub plan. The free plan supports only North American companies (U.S. - Canada).",
        "isin_paid_required": "This software uses Finnhub's free API keys, not its paid API keys, so you cannot search using non-U.S. ISINs. Enter the ticker symbol or a U.S. ISIN.",

        # formatter.py e exporter.py
        "coverage_hint": "Note: company news is only available for North American (US - Canada) companies, and free-plan API keys only have ~1 year of historical news.",

        # main.py
        "fetching_news": "Fetching market news for '{query}'...",
        "error_prefix": "Error:",
        "warning_prefix": "Warning:",
        "unsupported_output_format": "Unsupported file format. See available formats with: finuntius --help",
        "cli_desc": "CLI Terminal for real-time financial news via Finnhub API.",
        "cli_epilog": "\033[2;3mTo use Finuntius, a Finnhub API key is required (the free plan is sufficient).\nGet your free API key by creating an account at: https://finnhub.io/\n* Disclaimer: Finuntius is an independent open-source project and is not affiliated, endorsed, or sponsored by Finnhub.\033[0m\n\n\033[2mfinuntius \u00a9 g-projectech \u00b7 https://github.com/g-projectech/finuntius\033[0m",
        "group_positional": "positional arguments",
        "group_general": "general & configuration",
        "search_parameters": "search parameters",
        "output_group": "output & export",
        "cli_help_query": "Stock Ticker Symbol or US ISIN (e.g. AAPL)",
        "cli_help_h": "Show this help message and exit",
        "cli_help_v": "Show program's version number and exit",
        "cli_help_l": "Maximum number of news items to display (default: 5)",
        "cli_help_k": "Finnhub API Key",
        "cli_help_d": "Lookback period in days (default: 7)",
        "cli_help_j": "Output news in JSON format",
        "cli_help_m": "Output news in raw Markdown format (ideal for LLM prompts)",
        "cli_help_o": "Save output directly to a file (e.g., news.json or news.md)",
        "cli_help_c": "Interactively choose the display language and save it for future runs",
        "cli_req_query": "The following arguments are required: QUERY",
        "cli_conflicting_format": "Please select only one output format (-j or -m). For more info: finuntius -h",
        "cli_invalid_limit": "-l/--limit must be a positive integer (got {value}).",
        "cli_invalid_days": "-d/--days must be a positive integer (got {value}).",
        "cli_days_too_large": "-d/--days is too large (got {value}); the maximum lookback is {max} days.",
        "cli_ext_mismatch_json": "-j requires a .json output file, but got '{ext}'. Drop the extension to auto-add .json, or fix it.",
        "cli_ext_mismatch_md": "-m requires a .md output file, but got '{ext}'. Drop the extension to auto-add .md, or fix it.",
    },
    "it": {
        # config.py - configurazione API key
        "api_key_missing": "Chiave API Finnhub non trovata.",
        "api_key_intro": "Per usare Finuntius è richiesta una chiave API Finnhub (il piano gratuito è sufficiente).",
        "api_key_get_it": "Ottieni la tua chiave API gratuita creando un account su:",
        "disclaimer": "* Disclaimer: Finuntius è un progetto open-source indipendente e non è affiliato, sponsorizzato o approvato da Finnhub.",
        "prompt_api_key": "Inserisci la tua chiave API Finnhub",
        "api_key_empty_error": "La chiave API non puo' essere vuota.",
        "api_key_saved": "Chiave API salvata con successo in:",

        # config.py
        "language_saved": "Lingua impostata su:",
        "language_already_set": "Lingua attualmente in uso su Finuntius:",
        "language_option_english": "English",
        "language_option_italian": "Italiano",
        "language_prompt_label": "Seleziona lingua",
        "language_selection_title": "Seleziona la lingua",

        #formatter.py
        "panel_subtitle": "Terminale di Notizie Finanziarie (Tramite API Finnhub)",
        "panel_target_label": "Target:",
        "panel_results_label": "Risultati Trovati:",
        "no_news_found": "Nessuna notizia finanziaria trovata per il target:",
        "table_header_num": "#",
        "table_header_headline": "Titolo",
        "table_header_source": "Fonte",
        "table_header_date": "Data (UTC)",
        "table_header_url": "URL",

        #exporter.py
        "export_title": "Notizie Finanziarie per {target}",
        "export_fetched_at": "Recuperato il:",
        "export_total_results": "Risultati Totali:",
        "export_source": "Fonte:",
        "export_date": "Data (UTC):",
        "export_url": "URL:",
        "export_summary": "Riepilogo:",
        "export_no_news": "Nessuna notizia finanziaria trovata per {target}.",
        "output_saved": "Output salvato con successo in:",

        # finnhub_fetcher.py
        "missing_api_key": "Chiave API mancante. Imposta la variabile d'ambiente 'FINNHUB_API_KEY' oppure passala con '--api-key'.",
        "invalid_api_key": "Chiave API Finnhub non valida o scaduta.",
        "rate_limit": "Limite di richieste Finnhub raggiunto. Controlla i limiti del tuo piano sulla dashboard Finnhub (tutti i piani condividono un tetto di 30 richieste/secondo).",
        "unexpected_response": "Risposta API inattesa: {data}",
        "network_error": "Errore di rete durante la connessione a Finnhub: {err}",
        "isin_not_found": "Nessuna azienda trovata per l'ISIN '{isin}'.",
        "premium_ticker_required": "Questo ticker richiede un piano Finnhub a pagamento. Il piano gratuito supporta solo aziende nordamericane (USA - Canada).",
        "isin_paid_required": "Questo software si basa su API key gratuite di Finnhub, non su API key di Finnhub a pagamento, quindi non puoi cercare tramite ISIN non americani. Inserisci il ticker o un ISIN USA.",


        # formatter.py e exporter.py
        "coverage_hint": "Nota: le notizie aziendali sono disponibili solo per aziende nordamericane (USA - Canada); con chiavi API del piano gratuito, inoltre, la cronologia copre solo circa 1 anno.",

        # main.py
        "fetching_news": "Recupero notizie di mercato per '{query}'...",
        "error_prefix": "Errore:",
        "warning_prefix": "Attenzione:",
        "unsupported_output_format": "Formato file non disponibile. Vedi i formati disponibili con: finuntius --help",
        "cli_desc": "Terminale CLI per notizie finanziarie in tempo reale tramite API Finnhub.",
        "cli_epilog": "\033[2;3mPer usare Finuntius è richiesta una chiave API Finnhub (il piano gratuito è sufficiente).\nOttieni la tua chiave API gratuita creando un account su: https://finnhub.io/\n* Disclaimer: Finuntius è un progetto open-source indipendente e non è affiliato, sponsorizzato o approvato da Finnhub.\033[0m\n\n\033[2mfinuntius \u00a9 g-projectech \u00b7 https://github.com/g-projectech/finuntius\033[0m",
        "group_positional": "argomenti posizionali",
        "group_general": "generali e configurazione",
        "search_parameters": "parametri di ricerca",
        "output_group": "output e salvataggio",
        "cli_help_query": "Simbolo Ticker azionario o ISIN USA (es. AAPL)",
        "cli_help_h": "Mostra questo messaggio di aiuto ed esce",
        "cli_help_v": "Mostra la versione del programma ed esce",
        "cli_help_l": "Numero massimo di notizie da mostrare (default: 5)",
        "cli_help_k": "Chiave API Finnhub",
        "cli_help_d": "Periodo di retrospettiva in giorni (default: 7)",
        "cli_help_j": "Stampa le notizie in formato JSON",
        "cli_help_m": "Stampa le notizie in formato Markdown grezzo (ideale per prompt LLM)",
        "cli_help_o": "Salva l'output direttamente in un file (es. news.json o news.md)",
        "cli_help_c": "Scegli in modo interattivo la lingua del display e salvala per i futuri avvii",
        "cli_req_query": "I seguenti argomenti sono richiesti: QUERY",
        "cli_conflicting_format": "Seleziona un solo formato di output (-j o -m). Per maggiori informazioni: finuntius -h",
        "cli_invalid_limit": "-l/--limit deve essere un numero intero positivo (ricevuto {value}).",
        "cli_invalid_days": "-d/--days deve essere un numero intero positivo (ricevuto {value}).",
        "cli_days_too_large": "-d/--days è troppo grande (ricevuto {value}); il massimo consentito è {max} giorni.",
        "cli_ext_mismatch_json": "-j richiede un file di output .json, ma è stato indicato '{ext}'. Ometti l'estensione per aggiungere .json automaticamente, oppure correggila.",
        "cli_ext_mismatch_md": "-m richiede un file di output .md, ma è stato indicato '{ext}'. Ometti l'estensione per aggiungere .md automaticamente, oppure correggila.",
    },
}
#function t traduce i risultati nella lingua selezionata dall'utente
def t(key: str, language: str = DEFAULT_LANGUAGE, **kwargs) -> str:
    strings = TRANSLATIONS.get(language, TRANSLATIONS[DEFAULT_LANGUAGE])
    template = strings.get(key, TRANSLATIONS[DEFAULT_LANGUAGE].get(key, key))
    return template.format(**kwargs) if kwargs else template
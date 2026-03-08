from __future__ import annotations

from pathlib import Path

try:
    import pandas as pd
except Exception:  # pragma: no cover
    pd = None  # type: ignore


class TradingAssistant:
    """Analyze a trading journal CSV/XLSX file."""

    def analyze_journal(self, path: str) -> str:
        if pd is None:
            return "pandas is not installed; trading journal analysis unavailable."

        file_path = Path(path)
        if not file_path.exists():
            return f"Trading journal not found: {path}"

        df = self._load_dataframe(file_path)
        if df is None or df.empty:
            return "Trading journal is empty or unreadable."

        normalized = {col.lower().strip(): col for col in df.columns}
        if "pnl" not in normalized:
            return "Trading journal must include a 'pnl' column."

        pnl_col = normalized["pnl"]
        pnl = pd.to_numeric(df[pnl_col], errors="coerce").dropna()
        if pnl.empty:
            return "No valid numeric values in 'pnl' column."

        win_rate = float((pnl > 0).mean() * 100)
        avg_pnl = float(pnl.mean())
        total_pnl = float(pnl.sum())
        best_trade = float(pnl.max())
        worst_trade = float(pnl.min())

        return (
            "Trading Journal Analysis\n"
            f"- Trades analyzed: {len(pnl)}\n"
            f"- Win rate: {win_rate:.2f}%\n"
            f"- Average PnL: {avg_pnl:.2f}\n"
            f"- Total PnL: {total_pnl:.2f}\n"
            f"- Best trade: {best_trade:.2f}\n"
            f"- Worst trade: {worst_trade:.2f}"
        )

    def _load_dataframe(self, path: Path):
        if path.suffix.lower() == ".csv":
            return pd.read_csv(path)
        if path.suffix.lower() in {".xlsx", ".xls"}:
            return pd.read_excel(path)
        return None

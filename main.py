import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict


# ---------------------------
# 1. Текущая доходность (Current Yield)
# ---------------------------
def current_yield(price: float, coupon: float, payments_per_year: int = 2) -> float:
    annual_coupon = coupon * payments_per_year
    return annual_coupon / price


# ---------------------------
# 2. Доходность к погашению (YTM)
# ---------------------------
def ytm(price: float, coupon: float, years: float, nominal: float = 1000, payments_per_year: int = 2) -> float:
    periods = int(years * payments_per_year)
    cash_flows = np.array([coupon] * periods)
    cash_flows[-1] += nominal  # добавляем номинал в последнем периоде

    def npv(rate):
        return np.sum(cash_flows / (1 + rate / payments_per_year) ** np.arange(1, periods + 1)) - price

    # Поиск корня методом Ньютона
    guess = 0.15
    for _ in range(100):
        f = npv(guess)
        d = (npv(guess + 1e-6) - f) / 1e-6  # численная производная
        if abs(d) < 1e-9:
            break
        guess -= f / d
        if abs(f) < 1e-6:
            break
    return guess


# ---------------------------
# 3. Реальная доходность (для линкеров)
# ---------------------------
def real_yield(nominal_ytm: float, inflation: float) -> float:
    return nominal_ytm - inflation


# ---------------------------
# 4. Флоатеры: купон как ставка + спред
# ---------------------------
def floater_coupon(base_rate: float, spread: float) -> float:
    return base_rate + spread


# ---------------------------
# 5. Сравнение нескольких облигаций
# ---------------------------
def analyze_bonds(bonds: List[Dict], inflation: float = 0.06, base_rate: float = 0.15):
    results = []
    for b in bonds:
        if b["type"] == "fixed":
            cy = current_yield(b["price"], b["coupon"], b.get("payments_per_year", 2))
            yt = ytm(b["price"], b["coupon"], b["years"], b.get("nominal", 1000), b.get("payments_per_year", 2))
            results.append({
                "name": b["name"],
                "type": "Fixed",
                "Current Yield": f"{cy * 100:.2f}%",
                "YTM": f"{yt * 100:.2f}%"
            })

        elif b["type"] == "linker":
            yt = ytm(b["price"], b["coupon"], b["years"], b.get("nominal", 1000), b.get("payments_per_year", 2))
            ry = real_yield(yt, inflation)
            results.append({
                "name": b["name"],
                "type": "Linker",
                "YTM": f"{yt * 100:.2f}%",
                "Real Yield": f"{ry * 100:.2f}%"
            })

        elif b["type"] == "floater":
            fc = floater_coupon(base_rate, b.get("spread", 0.0))
            results.append({
                "name": b["name"],
                "type": "Floater",
                "Coupon Now": f"{fc * 100:.2f}%"
            })
    return results


# ---------------------------
# Пример использования
# ---------------------------
if __name__ == "__main__":
    bonds = [
        {"name": "ОФЗ-26238", "type": "fixed", "price": 900, "coupon": 35, "years": 3},
        {"name": "ОФЗ-ИН 52002", "type": "linker", "price": 950, "coupon": 25, "years": 4},
        {"name": "ОФЗ-ПК 29015", "type": "floater", "price": 1000, "coupon": 0, "years": 5, "spread": 0.005}
    ]

    report = analyze_bonds(bonds, inflation=0.06, base_rate=0.15)

    # Красивый вывод в консоль
    for r in report:
        print(r)

    # Вывод в виде таблицы через pandas
    df = pd.DataFrame(report)
    print("\nТабличный вывод:")
    print(df)

    # ---------------------------
    # Визуализация доходностей
    # ---------------------------
    # 1. График YTM
    plt.figure(figsize=(8, 5))
    if 'YTM' in df:
        plt.bar(df['name'], df['YTM'].str.rstrip('%').astype(float), color='skyblue')
        plt.ylabel('Доходность к погашению (YTM), %')
        plt.title('Доходности облигаций')
        plt.show()

    # 2. Сравнение CY, YTM, Real Yield
    df_plot = df.copy()
    for col in ['Current Yield', 'YTM', 'Real Yield']:
        if col in df_plot:
            df_plot[col] = df_plot[col].str.rstrip('%').astype(float)

    df_melt = df_plot.melt(id_vars=['name'], value_vars=['Current Yield', 'YTM', 'Real Yield'], var_name='Показатель',
                           value_name='Значение').dropna()

    plt.figure(figsize=(10, 6))
    for label, subset in df_melt.groupby('Показатель'):
        plt.bar(subset['name'], subset['Значение'], label=label, alpha=0.7)

    plt.ylabel('Доходность, %')
    plt.title('Сравнение доходностей облигаций')
    plt.legend()
    plt.show()

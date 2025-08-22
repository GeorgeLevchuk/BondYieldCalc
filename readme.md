# Bond Yield Calculator

Эта программа на Python позволяет рассчитывать основные показатели доходности облигаций разных типов:

- **Фиксированные облигации (Fixed)** — расчёт текущей доходности (Current Yield) и доходности к погашению (YTM).
- **Линкеры (ОФЗ-ИН)** — облигации с индексируемым номиналом. Дополнительно считается реальная доходность (Real Yield) с учётом инфляции.
- **Флоатеры (ОФЗ-ПК)** — облигации с плавающим купоном. Купон пересчитывается как базовая ставка (RUONIA или ключевая ставка ЦБ) + спред.

## 🔢 Формулы

### 1. Текущая доходность (Current Yield)
$$
CY = \frac{C_{annual}}{P}
$$
где:  
- $C_{annual}$ — годовой купон,  
- $P$ — текущая цена облигации.

---

### 2. Доходность к погашению (Yield to Maturity, YTM)
$$
P = \sum_{t=1}^{N} \frac{C}{\left(1+\frac{YTM}{m}\right)^t} + \frac{NOM}{\left(1+\frac{YTM}{m}\right)^N}
$$
где:  
- $P$ — текущая цена облигации,  
- $C$ — купон за период,  
- $NOM$ — номинал облигации,  
- $m$ — количество купонных выплат в год,  
- $N$ — общее число выплат до погашения.

---

### 3. Реальная доходность (для линкеров)
$$
RY = YTM - \pi
$$
где:  
- $YTM$ — номинальная доходность к погашению,  
- $\pi$ — уровень инфляции.

---

### 4. Флоатеры (купон)
$$
Coupon = BaseRate + Spread
$$
где:  
- $BaseRate$ — базовая ставка (например, ключевая ставка ЦБ),  
- $Spread$ — фиксированная надбавка.

## ⚙️ Использование

Пример данных для анализа:
```python
bonds = [
    {"name": "ОФЗ-26238", "type": "fixed", "price": 900, "coupon": 35, "years": 3},
    {"name": "ОФЗ-ИН 52002", "type": "linker", "price": 950, "coupon": 25, "years": 4},
    {"name": "ОФЗ-ПК 29015", "type": "floater", "price": 1000, "coupon": 0, "years": 5, "spread": 0.005}
]

report = analyze_bonds(bonds, inflation=0.06, base_rate=0.15)
for r in report:
    print(r)
```

## 📊 Пример вывода в консоли
```text
{'name': 'ОФЗ-26238', 'type': 'Fixed', 'Current Yield': '7.78%', 'YTM': '14.82%'}
{'name': 'ОФЗ-ИН 52002', 'type': 'Linker', 'YTM': '13.21%', 'Real Yield': '7.21%'}
{'name': 'ОФЗ-ПК 29015', 'type': 'Floater', 'Coupon Now': '15.50%'}
```

## 📑 Красивый вывод через Pandas
```python
import pandas as pd

report = analyze_bonds(bonds, inflation=0.06, base_rate=0.15)
df = pd.DataFrame(report)
print(df)
```

### Пример табличного вывода:
```
        name     type Current Yield     YTM Real Yield Coupon Now
0  ОФЗ-26238    Fixed         7.78%  14.82%       NaN       NaN
1  ОФЗ-ИН 52002 Linker          NaN  13.21%     7.21%       NaN
2  ОФЗ-ПК 29015 Floater        NaN     NaN       NaN    15.50%
```

## 📈 Визуализация доходностей
### График YTM
```python
import matplotlib.pyplot as plt
import pandas as pd

report = analyze_bonds(bonds, inflation=0.06, base_rate=0.15)
df = pd.DataFrame(report)

plt.figure(figsize=(8,5))
plt.bar(df['name'], df['YTM'].str.rstrip('%').astype(float), color='skyblue')
plt.ylabel('Доходность к погашению (YTM), %')
plt.title('Доходности облигаций')
plt.show()
```

### Сравнение доходностей (CY, YTM, Real Yield)
```python
import matplotlib.pyplot as plt
import pandas as pd

report = analyze_bonds(bonds, inflation=0.06, base_rate=0.15)
df = pd.DataFrame(report)

# Преобразуем проценты в float
for col in ["Current Yield", "YTM", "Real Yield"]:
    if col in df:
        df[col] = df[col].str.rstrip('%').astype(float)

# Построим сравнение
plt.figure(figsize=(10,6))
df_plot = df.melt(id_vars=["name"], value_vars=["Current Yield", "YTM", "Real Yield"], var_name="Показатель", value_name="Значение")
df_plot = df_plot.dropna()

for label, subset in df_plot.groupby("Показатель"):
    plt.bar(subset["name"], subset["Значение"], label=label, alpha=0.7)

plt.ylabel('Доходность, %')
plt.title('Сравнение доходностей облигаций')
plt.legend()
plt.show()
```

---

## 🛠 Возможности
- Расчёт **CY, YTM, Real Yield, Floater Coupon**.
- Поддержка **разных типов облигаций**.
- Гибкость: можно указать инфляцию, базовую ставку и количество купонных выплат в год.
- Красивый вывод результатов в **табличной форме**.
- Визуализация доходностей на графиках (YTM и сравнение разных показателей).

## 🔮 Дальнейшие улучшения
- Интеграция с API Московской биржи для автоматической загрузки цен и доходностей.

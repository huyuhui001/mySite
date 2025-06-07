# Polars入门简介

## 安装 Polars

参考:

- [Polars user guide](https://docs.pola.rs/)
- [Github: pola-rs/polars](https://github.com/pola-rs/polars)

```python
pip install polars
```

## 读写数据

Polars支持读取和写入常见文件格式（csv，JSON，等）和数据库（PostgreSQL，MySQL，等）。

下面是一个简单的处理数据集的示例代码。

```python
import polars as pl
import datetime as dt

df = pl.DataFrame(
    {
        "name": ["Alice Archer", "Ben Brown", "Chloe Cooper", "Daniel Donovan"],
        "birthdate": [dt.date(1997, 1, 10),
                      dt.date(1985, 2, 15),
                      dt.date(1983, 3, 22),
                      dt.date(1981, 4, 30)],
        "weight": [57.9, 72.5, 53.6, 83.1],  # (kg)
        "height": [1.56, 1.77, 1.65, 1.75],   # (m)
    }
)
print(df)
```

输出结果：

```console
shape: (4, 4)
┌────────────────┬────────────┬────────┬────────┐
│ name           ┆ birthdate  ┆ weight ┆ height │
│ ---            ┆ ---        ┆ ---    ┆ ---    │
│ str            ┆ date       ┆ f64    ┆ f64    │
╞════════════════╪════════════╪════════╪════════╡
│ Alice Archer   ┆ 1997-01-10 ┆ 57.9   ┆ 1.56   │
│ Ben Brown      ┆ 1985-02-15 ┆ 72.5   ┆ 1.77   │
│ Chloe Cooper   ┆ 1983-03-22 ┆ 53.6   ┆ 1.65   │
│ Daniel Donovan ┆ 1981-04-30 ┆ 83.1   ┆ 1.75   │
└────────────────┴────────────┴────────┴────────┘
```

修改上面代码，将数据集先写入文件，再从文件读取并显示。

```python
import polars as pl
import datetime as dt

df = pl.DataFrame(
    {
        "name": ["Alice Archer", "Ben Brown", "Chloe Cooper", "Daniel Donovan"],
        "birthdate": [dt.date(1997, 1, 10),
                      dt.date(1985, 2, 15),
                      dt.date(1983, 3, 22),
                      dt.date(1981, 4, 30)],
        "weight": [57.9, 72.5, 53.6, 83.1],  # (kg)
        "height": [1.56, 1.77, 1.65, 1.75],   # (m)
    }
)

file_name = "./assets/polars_output.csv"
df.write_csv(file_name)

df_csv = pl.read_csv(file_name, try_parse_dates=True)
print(df_csv)
```

输出结果：

```console
shape: (4, 4)
┌────────────────┬────────────┬────────┬────────┐
│ name           ┆ birthdate  ┆ weight ┆ height │
│ ---            ┆ ---        ┆ ---    ┆ ---    │
│ str            ┆ date       ┆ f64    ┆ f64    │
╞════════════════╪════════════╪════════╪════════╡
│ Alice Archer   ┆ 1997-01-10 ┆ 57.9   ┆ 1.56   │
│ Ben Brown      ┆ 1985-02-15 ┆ 72.5   ┆ 1.77   │
│ Chloe Cooper   ┆ 1983-03-22 ┆ 53.6   ┆ 1.65   │
│ Daniel Donovan ┆ 1981-04-30 ┆ 83.1   ┆ 1.75   │
└────────────────┴────────────┴────────┴────────┘
```

文件`polars_output.csv`的内容：

```csv
name,birthdate,weight,height
Alice Archer,1997-01-10,57.9,1.56
Ben Brown,1985-02-15,72.5,1.77
Chloe Cooper,1983-03-22,53.6,1.65
Daniel Donovan,1981-04-30,83.1,1.75
```

## `select`

表达式是 Polars 的主要优势之一，因为它提供了一种模块化和灵活的方式来表达数据转换。

下面是一个 Polars 表达式的例子。通过`select`来选择并操作数据帧中的列。

```python
import polars as pl
import datetime as dt

df = pl.DataFrame(
    {
        "name": ["Alice Archer", "Ben Brown", "Chloe Cooper", "Daniel Donovan"],
        "birthdate": [dt.date(1997, 1, 10),
                      dt.date(1985, 2, 15),
                      dt.date(1983, 3, 22),
                      dt.date(1981, 4, 30)],
        "weight": [57.9, 72.5, 53.6, 83.1],  # (kg)
        "height": [1.56, 1.77, 1.65, 1.75],   # (m)
    }
)

result = df.select(
    pl.col("name"),
    pl.col("birthdate").dt.year().alias("birth_year"),
    (pl.col("weight") / (pl.col("height") ** 2)).alias("bmi"),
)

file_name = "./assets/polars_output.csv"
result.write_csv(file_name)

df_csv = pl.read_csv(file_name, try_parse_dates=True)
print(df_csv)
```

运行结果：

```console
shape: (4, 3)
┌────────────────┬────────────┬───────────┐
│ name           ┆ birth_year ┆ bmi       │
│ ---            ┆ ---        ┆ ---       │
│ str            ┆ i64        ┆ f64       │
╞════════════════╪════════════╪═══════════╡
│ Alice Archer   ┆ 1997       ┆ 23.791913 │
│ Ben Brown      ┆ 1985       ┆ 23.141498 │
│ Chloe Cooper   ┆ 1983       ┆ 19.687787 │
│ Daniel Donovan ┆ 1981       ┆ 27.134694 │
└────────────────┴────────────┴───────────┘
```

Polars 还支持“表达式扩展”（expression expansion）的特性，其中一个表达式充当多个表达式的简写形式。
在下面的例子中，我们使用表达式扩展通过单个表达式`pl.col("weight", "height")`操作 "weight" 和 "height" 两列。
使用表达式扩展时，可以使用 `.name.suffix` 为原始列名添加后缀。

```python
import polars as pl
import datetime as dt

df = pl.DataFrame(
    {
        "name": ["Alice Archer", "Ben Brown", "Chloe Cooper", "Daniel Donovan"],
        "birthdate": [dt.date(1997, 1, 10),
                      dt.date(1985, 2, 15),
                      dt.date(1983, 3, 22),
                      dt.date(1981, 4, 30)],
        "weight": [57.9, 72.5, 53.6, 83.1],  # (kg)
        "height": [1.56, 1.77, 1.65, 1.75],   # (m)
    }
)

result = df.select(
    pl.col("name"),
    pl.col("birthdate").dt.year().alias("birth_year"),
    (pl.col("weight") / (pl.col("height") ** 2)).alias("bmi"),
    (pl.col("weight", "height") * 0.95).round(2).name.suffix("-5%"),
)

file_name = "./assets/polars_output.csv"
result.write_csv(file_name)

df_csv = pl.read_csv(file_name, try_parse_dates=True)
print(df_csv)
```

运行结果：

```console
shape: (4, 5)
┌────────────────┬────────────┬───────────┬───────────┬───────────┐
│ name           ┆ birth_year ┆ bmi       ┆ weight-5% ┆ height-5% │
│ ---            ┆ ---        ┆ ---       ┆ ---       ┆ ---       │
│ str            ┆ i64        ┆ f64       ┆ f64       ┆ f64       │
╞════════════════╪════════════╪═══════════╪═══════════╪═══════════╡
│ Alice Archer   ┆ 1997       ┆ 23.791913 ┆ 55.0      ┆ 1.48      │
│ Ben Brown      ┆ 1985       ┆ 23.141498 ┆ 68.88     ┆ 1.68      │
│ Chloe Cooper   ┆ 1983       ┆ 19.687787 ┆ 50.92     ┆ 1.57      │
│ Daniel Donovan ┆ 1981       ┆ 27.134694 ┆ 78.94     ┆ 1.66      │
└────────────────┴────────────┴───────────┴───────────┴───────────┘
```

## `with_columns`

`with_columns` 上下文与 `select` 上下文非常相似，但 `with_columns` 是向数据帧添加列，而不是选择列。
注意下面运行结果，是在原有数据列的基础上，额外引入了两个新列`birth_year`和`bmi`：

```python
import polars as pl
import datetime as dt

df = pl.DataFrame(
    {
        "name": ["Alice Archer", "Ben Brown", "Chloe Cooper", "Daniel Donovan"],
        "birthdate": [dt.date(1997, 1, 10),
                      dt.date(1985, 2, 15),
                      dt.date(1983, 3, 22),
                      dt.date(1981, 4, 30)],
        "weight": [57.9, 72.5, 53.6, 83.1],  # (kg)
        "height": [1.56, 1.77, 1.65, 1.75],   # (m)
    }
)


result = df.with_columns(
    birth_year=pl.col("birthdate").dt.year(),
    bmi=pl.col("weight") / (pl.col("height") ** 2),
)

file_name = "./assets/polars_output.csv"
result.write_csv(file_name)

df_csv = pl.read_csv(file_name, try_parse_dates=True)
print(df_csv)
```

运行结果：

```console
shape: (4, 6)
┌────────────────┬────────────┬────────┬────────┬────────────┬───────────┐
│ name           ┆ birthdate  ┆ weight ┆ height ┆ birth_year ┆ bmi       │
│ ---            ┆ ---        ┆ ---    ┆ ---    ┆ ---        ┆ ---       │
│ str            ┆ date       ┆ f64    ┆ f64    ┆ i64        ┆ f64       │
╞════════════════╪════════════╪════════╪════════╪════════════╪═══════════╡
│ Alice Archer   ┆ 1997-01-10 ┆ 57.9   ┆ 1.56   ┆ 1997       ┆ 23.791913 │
│ Ben Brown      ┆ 1985-02-15 ┆ 72.5   ┆ 1.77   ┆ 1985       ┆ 23.141498 │
│ Chloe Cooper   ┆ 1983-03-22 ┆ 53.6   ┆ 1.65   ┆ 1983       ┆ 19.687787 │
│ Daniel Donovan ┆ 1981-04-30 ┆ 83.1   ┆ 1.75   ┆ 1981       ┆ 27.134694 │
└────────────────┴────────────┴────────┴────────┴────────────┴───────────┘
```

上面代码中`df.with_columns()`这一段也可以用下面的写法。

```python
result = df.with_columns(
    pl.col("birthdate").dt.year().alias("birth_year"),
    (pl.col("weight") / (pl.col("height") ** 2)).alias("bmi"),
)
```

## `filter`

`filter`上下文可以用来创建一个包含原始数据行的子集，即基于某列进行条件筛选。
下例中`result.filter(pl.col("birthdate").dt.year() < 1990)`是对`birthdate`进行条件筛选，符合条件的子集（`< 1990`）会显示打印出来。

```python
import polars as pl
import datetime as dt

df = pl.DataFrame(
    {
        "name": ["Alice Archer", "Ben Brown", "Chloe Cooper", "Daniel Donovan"],
        "birthdate": [dt.date(1997, 1, 10),
                      dt.date(1985, 2, 15),
                      dt.date(1983, 3, 22),
                      dt.date(1981, 4, 30)],
        "weight": [57.9, 72.5, 53.6, 83.1],  # (kg)
        "height": [1.56, 1.77, 1.65, 1.75],   # (m)
    }
)


result = df.with_columns(
    birth_year=pl.col("birthdate").dt.year(),
    bmi=pl.col("weight") / (pl.col("height") ** 2),
)

result = result.filter(pl.col("birthdate").dt.year() < 1990)
print(result)

file_name = "./assets/polars_output.csv"
result.write_csv(file_name)

df_csv = pl.read_csv(file_name, try_parse_dates=True)
print(df_csv)
```

运行结果：

```console
shape: (3, 6)
┌────────────────┬────────────┬────────┬────────┬────────────┬───────────┐
│ name           ┆ birthdate  ┆ weight ┆ height ┆ birth_year ┆ bmi       │
│ ---            ┆ ---        ┆ ---    ┆ ---    ┆ ---        ┆ ---       │
│ str            ┆ date       ┆ f64    ┆ f64    ┆ i64        ┆ f64       │
╞════════════════╪════════════╪════════╪════════╪════════════╪═══════════╡
│ Ben Brown      ┆ 1985-02-15 ┆ 72.5   ┆ 1.77   ┆ 1985       ┆ 23.141498 │
│ Chloe Cooper   ┆ 1983-03-22 ┆ 53.6   ┆ 1.65   ┆ 1983       ┆ 19.687787 │
│ Daniel Donovan ┆ 1981-04-30 ┆ 83.1   ┆ 1.75   ┆ 1981       ┆ 27.134694 │
└────────────────┴────────────┴────────┴────────┴────────────┴───────────┘
```

上面代码可以简写为：

```python
result = df.with_columns(
    birth_year=pl.col("birthdate").dt.year(),
    bmi=pl.col("weight") / (pl.col("height") ** 2),
).filter(pl.col("birthdate").dt.year() < 1990)
```

我们也可以将多个谓词表达式作为单独的参数提供`is_between(dt.date(1982, 12, 31), dt.date(1996, 1, 1))`，这比用 `&` 将它们组合在一起`(pl.col("birthdate").dt.year() > 1982) & (pl.col("birthdate").dt.year() < 1996)`更方便。

```python
import polars as pl
import datetime as dt

df = pl.DataFrame(
    {
        "name": ["Alice Archer", "Ben Brown", "Chloe Cooper", "Daniel Donovan"],
        "birthdate": [
            dt.date(1997, 1, 10),
            dt.date(1985, 2, 15),
            dt.date(1983, 3, 22),
            dt.date(1981, 4, 30),
        ],
        "weight": [57.9, 72.5, 53.6, 83.1],  # (kg)
        "height": [1.56, 1.77, 1.65, 1.75],  # (m)
    }
)


result = df.with_columns(
    birth_year=pl.col("birthdate").dt.year(),
    bmi=pl.col("weight") / (pl.col("height") ** 2),
).filter(
    pl.col("birthdate").is_between(dt.date(1982, 12, 31), dt.date(1996, 1, 1)),
    pl.col("height") > 1.7,
)

file_name = "./assets/polars_output.csv"
result.write_csv(file_name)

df_csv = pl.read_csv(file_name, try_parse_dates=True)
print(df_csv)
```

运行结果：

```console
shape: (1, 6)
┌───────────┬────────────┬────────┬────────┬────────────┬───────────┐
│ name      ┆ birthdate  ┆ weight ┆ height ┆ birth_year ┆ bmi       │
│ ---       ┆ ---        ┆ ---    ┆ ---    ┆ ---        ┆ ---       │
│ str       ┆ date       ┆ f64    ┆ f64    ┆ i64        ┆ f64       │
╞═══════════╪════════════╪════════╪════════╪════════════╪═══════════╡
│ Ben Brown ┆ 1985-02-15 ┆ 72.5   ┆ 1.77   ┆ 1985       ┆ 23.141498 │
└───────────┴────────────┴────────┴────────┴────────────┴───────────┘
```

## group_by

`group_by`上下文可用于将数据集中一个或多个表达式值相同的行分组在一起。下面的例子计算每个十年出生的人数：

```python
import polars as pl
import datetime as dt

df = pl.DataFrame(
    {
        "name": ["Alice Archer", "Ben Brown", "Chloe Cooper", "Daniel Donovan"],
        "birthdate": [
            dt.date(1997, 1, 10),
            dt.date(1985, 2, 15),
            dt.date(1983, 3, 22),
            dt.date(1981, 4, 30),
        ],
        "weight": [57.9, 72.5, 53.6, 83.1],  # (kg)
        "height": [1.56, 1.77, 1.65, 1.75],  # (m)
    }
)


result = df.group_by(
    (pl.col("birthdate").dt.year() // 10 * 10).alias("decade"),
    maintain_order=True,
).len()

file_name = "./assets/polars_output.csv"
result.write_csv(file_name)

df_csv = pl.read_csv(file_name, try_parse_dates=True)
print(df_csv)
```

运行结果：

```console
shape: (2, 2)
┌────────┬─────┐
│ decade ┆ len │
│ ---    ┆ --- │
│ i64    ┆ i64 │
╞════════╪═════╡
│ 1990   ┆ 1   │
│ 1980   ┆ 3   │
└────────┴─────┘
```

在使用 `group_by` 上下文之后，我们可以使用 `agg` 来计算结果分组的聚合值：

```python
import polars as pl
import datetime as dt

df = pl.DataFrame(
    {
        "name": ["Alice Archer", "Ben Brown", "Chloe Cooper", "Daniel Donovan"],
        "birthdate": [
            dt.date(1997, 1, 10),
            dt.date(1985, 2, 15),
            dt.date(1983, 3, 22),
            dt.date(1981, 4, 30),
        ],
        "weight": [57.9, 72.5, 53.6, 83.1],  # (kg)
        "height": [1.56, 1.77, 1.65, 1.75],  # (m)
    }
)


result = df.group_by(
    (pl.col("birthdate").dt.year() // 10 * 10).alias("decade"),
    maintain_order=True,
).agg(
    pl.len().alias("sample_size"),
    pl.col("weight").mean().round(2).alias("avg_weight"),
    pl.col("height").max().alias("tallest"),
)

file_name = "./assets/polars_output.csv"
result.write_csv(file_name)

df_csv = pl.read_csv(file_name, try_parse_dates=True)
print(df_csv)
```

运行结果：

```console
shape: (2, 4)
┌────────┬─────────────┬────────────┬─────────┐
│ decade ┆ sample_size ┆ avg_weight ┆ tallest │
│ ---    ┆ ---         ┆ ---        ┆ ---     │
│ i64    ┆ i64         ┆ f64        ┆ f64     │
╞════════╪═════════════╪════════════╪═════════╡
│ 1990   ┆ 1           ┆ 57.9       ┆ 1.56    │
│ 1980   ┆ 3           ┆ 69.73      ┆ 1.77    │
└────────┴─────────────┴────────────┴─────────┘
```

## 复杂的查询

基于上面所列举的`selct`，`filter`等上下文及其内部的表达式可以链接起来，我们可以创建更复杂的查询。更详细的表达式，参考链接<https://docs.pola.rs/user-guide/expressions/>

```python
import polars as pl
import datetime as dt

df = pl.DataFrame(
    {
        "name": ["Alice Archer", "Ben Brown", "Chloe Cooper", "Daniel Donovan"],
        "birthdate": [
            dt.date(1997, 1, 10),
            dt.date(1985, 2, 15),
            dt.date(1983, 3, 22),
            dt.date(1981, 4, 30),
        ],
        "weight": [57.9, 72.5, 53.6, 83.1],  # (kg)
        "height": [1.56, 1.77, 1.65, 1.75],  # (m)
    }
)


result = (
    df.with_columns(
        (pl.col("birthdate").dt.year() // 10 * 10).alias("decade"),
        pl.col("name").str.split(by=" ").list.first(),
    )
    .select(pl.all().exclude("birthdate"))
    .group_by(
        pl.col("decade"),
        maintain_order=True,
    )
    .agg(
        pl.col("name"),
        pl.col("weight", "height").mean().round(2).name.prefix("avg_"),
    )
)

print(result)
```

运行结果：

```console
shape: (2, 4)
┌────────┬────────────────────────────┬────────────┬────────────┐
│ decade ┆ name                       ┆ avg_weight ┆ avg_height │
│ ---    ┆ ---                        ┆ ---        ┆ ---        │
│ i32    ┆ list[str]                  ┆ f64        ┆ f64        │
╞════════╪════════════════════════════╪════════════╪════════════╡
│ 1990   ┆ ["Alice"]                  ┆ 57.9       ┆ 1.56       │
│ 1980   ┆ ["Ben", "Chloe", "Daniel"] ┆ 69.73      ┆ 1.72       │
└────────┴────────────────────────────┴────────────┴────────────┘
```

## 组合数据

更详细的变换组合，参考链接<https://docs.pola.rs/user-guide/transformations/>。

### 连接join

下面的例子演示了当某列可以作为唯一标识符来建立两个数据集的行之间的对应关系时，如何使用左外连接（left outer join）来组合两个数据帧：

```python
import polars as pl
import datetime as dt

df = pl.DataFrame(
    {
        "name": ["Alice Archer", "Ben Brown", "Chloe Cooper", "Daniel Donovan"],
        "birthdate": [
            dt.date(1997, 1, 10),
            dt.date(1985, 2, 15),
            dt.date(1983, 3, 22),
            dt.date(1981, 4, 30),
        ],
        "weight": [57.9, 72.5, 53.6, 83.1],  # (kg)
        "height": [1.56, 1.77, 1.65, 1.75],  # (m)
    }
)

df2 = pl.DataFrame(
    {
        "name": ["James Bond", "Daniel Donovan", "Alice Archer", "Chloe Cooper"],
        "parent": [True, False, False, False],
        "siblings": [1, 2, 3, 4],
    }
)

print(df.join(df2, on="name", how="left"))
```

`df`的数据：

```console
shape: (4, 4)
┌────────────────┬────────────┬────────┬────────┐
│ name           ┆ birthdate  ┆ weight ┆ height │
│ ---            ┆ ---        ┆ ---    ┆ ---    │
│ str            ┆ date       ┆ f64    ┆ f64    │
╞════════════════╪════════════╪════════╪════════╡
│ Alice Archer   ┆ 1997-01-10 ┆ 57.9   ┆ 1.56   │
│ Ben Brown      ┆ 1985-02-15 ┆ 72.5   ┆ 1.77   │
│ Chloe Cooper   ┆ 1983-03-22 ┆ 53.6   ┆ 1.65   │
│ Daniel Donovan ┆ 1981-04-30 ┆ 83.1   ┆ 1.75   │
└────────────────┴────────────┴────────┴────────┘
```

`df2`的数据：

```console
shape: (4, 3)
┌────────────────┬────────┬──────────┐
│ name           ┆ parent ┆ siblings │
│ ---            ┆ ---    ┆ ---      │
│ str            ┆ bool   ┆ i64      │
╞════════════════╪════════╪══════════╡
│ James Bond     ┆ true   ┆ 1        │
│ Daniel Donovan ┆ false  ┆ 2        │
│ Alice Archer   ┆ false  ┆ 3        │
│ Chloe Cooper   ┆ false  ┆ 4        │
└────────────────┴────────┴──────────┘
```

`join`后的结果数据：

```console
shape: (4, 6)
┌────────────────┬────────────┬────────┬────────┬────────┬──────────┐
│ name           ┆ birthdate  ┆ weight ┆ height ┆ parent ┆ siblings │
│ ---            ┆ ---        ┆ ---    ┆ ---    ┆ ---    ┆ ---      │
│ str            ┆ date       ┆ f64    ┆ f64    ┆ bool   ┆ i64      │
╞════════════════╪════════════╪════════╪════════╪════════╪══════════╡
│ Alice Archer   ┆ 1997-01-10 ┆ 57.9   ┆ 1.56   ┆ false  ┆ 3        │
│ Ben Brown      ┆ 1985-02-15 ┆ 72.5   ┆ 1.77   ┆ null   ┆ null     │
│ Chloe Cooper   ┆ 1983-03-22 ┆ 53.6   ┆ 1.65   ┆ false  ┆ 4        │
│ Daniel Donovan ┆ 1981-04-30 ┆ 83.1   ┆ 1.75   ┆ false  ┆ 2        │
└────────────────┴────────────┴────────┴────────┴────────┴──────────┘
```

### 拼接

拼接数据集会创建一个更高（行更多）或更宽（列更多）的数据集，具体取决于使用的方法。

下面的示例中，我们使用垂直拼接来创建一个更高（行更多）的数据集。注意，垂直拼接会检查2个数据集的列的一致性，包括名称和数据类型，否则会报错。

```python
import polars as pl
import datetime as dt

df = pl.DataFrame(
    {
        "name": ["Alice Archer", "Ben Brown", "Chloe Cooper", "Daniel Donovan"],
        "birthdate": [
            dt.date(1997, 1, 10),
            dt.date(1985, 2, 15),
            dt.date(1983, 3, 22),
            dt.date(1981, 4, 30),
        ],
        "weight": [57.9, 72.5, 53.6, 83.1],  # (kg)
        "height": [1.56, 1.77, 1.65, 1.75],  # (m)
    }
)

df2 = pl.DataFrame(
    {
        "name": ["James Bond", "Daniel Donovan", "Alice Archer", "Chloe Cooper"],
        "parent": [True, False, False, False],
        "siblings": [1, 2, 3, 4],
    }
)

df3 = pl.DataFrame(
    {
        "name": ["Ethan Edwards", "Fiona Foster", "Grace Gibson", "Henry Harris"],
        "birthdate": [dt.date(1977, 5, 10),
                      dt.date(1975, 6, 23),
                      dt.date(1973, 7, 22),
                      dt.date(1971, 8, 3)],
        "weight": [67.9, 72.5, 57.6, 93.1],  # (kg)
        "height": [1.76, 1.6, 1.66, 1.8],     # (m)
    }
)

print(pl.concat([df, df3], how="vertical"))
```

运行结果：

```console
shape: (8, 4)
┌────────────────┬────────────┬────────┬────────┐
│ name           ┆ birthdate  ┆ weight ┆ height │
│ ---            ┆ ---        ┆ ---    ┆ ---    │
│ str            ┆ date       ┆ f64    ┆ f64    │
╞════════════════╪════════════╪════════╪════════╡
│ Alice Archer   ┆ 1997-01-10 ┆ 57.9   ┆ 1.56   │
│ Ben Brown      ┆ 1985-02-15 ┆ 72.5   ┆ 1.77   │
│ Chloe Cooper   ┆ 1983-03-22 ┆ 53.6   ┆ 1.65   │
│ Daniel Donovan ┆ 1981-04-30 ┆ 83.1   ┆ 1.75   │
│ Ethan Edwards  ┆ 1977-05-10 ┆ 67.9   ┆ 1.76   │
│ Fiona Foster   ┆ 1975-06-23 ┆ 72.5   ┆ 1.6    │
│ Grace Gibson   ┆ 1973-07-22 ┆ 57.6   ┆ 1.66   │
│ Henry Harris   ┆ 1971-08-03 ┆ 93.1   ┆ 1.8    │
└────────────────┴────────────┴────────┴────────┘
```

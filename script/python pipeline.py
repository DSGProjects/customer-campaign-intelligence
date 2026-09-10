import pandas as pd
import numpy as np


def sin_outliers(df, col):
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    IQR = q3 - q1
    limite_inferior = q1 - 1.5 * IQR
    limite_superior = q3 + 1.5 * IQR
    return df[(df[col] >= limite_inferior) & (df[col] <= limite_superior)]


def limpiar_datos(df):
    median_income = df["Income"].median()
    df["Income"] = df["Income"].fillna(median_income)

    df = sin_outliers(df, "Year_Birth")
    df = df[df["Income"] < 666666.0]

    df["Marital_Status"] = df["Marital_Status"].replace("Alone", "Single")
    df["Marital_Status"] = df["Marital_Status"].replace("Absurd", "Single")
    df["Marital_Status"] = df["Marital_Status"].replace("YOLO", "Single")

    df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"])
    df = df.drop(columns=["Z_CostContact", "Z_Revenue"])

    return df


def crear_features(df):
    df["Edad"] = 2014 - df["Year_Birth"]

    df["Gasto_Total"] = (
        df["MntWines"] + df["MntFruits"] + df["MntMeatProducts"]
        + df["MntFishProducts"] + df["MntSweetProducts"] + df["MntGoldProds"]
    )

    df["Compras_Totales"] = (
        df["NumWebPurchases"] + df["NumCatalogPurchases"] + df["NumStorePurchases"]
    )

    df["Campañas_Aceptadas"] = (
        df["AcceptedCmp1"] + df["AcceptedCmp2"] + df["AcceptedCmp3"]
        + df["AcceptedCmp4"] + df["AcceptedCmp5"]
    )

    df["Dependientes"] = df["Kidhome"] + df["Teenhome"]

    fecha_referencia = df["Dt_Customer"].max()
    df["Antiguedad_Cliente"] = (fecha_referencia - df["Dt_Customer"]).dt.days
    
    q33 = df["Gasto_Total"].quantile(0.33)
    q66 = df["Gasto_Total"].quantile(0.66)
    
    df["Segmento_Valor"] = pd.cut(
    df["Gasto_Total"],
    bins=[-1, q33, q66, df["Gasto_Total"].max()],
    labels=["Bajo", "Medio", "Alto"]
)

    return df


def main():
    df = pd.read_csv("../data/raw/marketing_campaign.csv", sep=";")

    df = limpiar_datos(df)
    df.to_csv("../data/processed/marketing_campaign_clean.csv", index=False)

    df = crear_features(df)
    df.to_csv("../data/processed/marketing_campaign_features.csv", index=False)


if __name__ == "__main__":
    main()
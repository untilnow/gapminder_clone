import sqlite3
import pandas as pd

class createGapminderDB:
    def __init__(self):
        self.file_names=["ddf--datapoints--gdp_pcap--by--country--time",
           "ddf--datapoints--lex--by--country--time",
           "ddf--datapoints--pop--by--country--time",
           "ddf--entities--geo--country"]
        self.table_names = ["gdp_per_capital", "life_expectancy", "population","geography"]
    def import_as_dataframe(self):
        df_dict= dict()
        for file_name,table_name in zip(self.file_names,self.table_names):
            file_path =f"data/{file_name}.csv"
            df=pd.read_csv(file_path)
            df_dict[table_name] = df
        return df_dict
    def create_database(self):
        connection = sqlite3.connect("data/gapminder.db")
        df_dict = self.import_as_dataframe()
        for k, v in df_dict.items():
            v.to_sql(name=k, con=connection, index=False, if_exists="replace")

        drop_view_sql = """
        DROP VIEW IF EXISTS plotting;
        """
        create_view_sql= """
        CREATE VIEW plotting AS
        Select geography.name as country_name,
                Geography.world_4region AS continent,
                gdp_per_capital.time AS dt_year,
                gdp_per_capital.gdp_pcap AS gdp_per_capita,
                life_expectancy.lex AS life_expectancy,
                population.pop AS population
            From gdp_per_capital
            join geography
            on gdp_per_capital.country = geography.country
            join population
            on gdp_per_capital.country = population.country AND
                gdp_per_capital.time= population.time
            join life_expectancy
            on gdp_per_capital.country = life_expectancy.country AND
                gdp_per_capital.time= life_expectancy.time
        Where gdp_per_capital.time< 2024
        """
        cur=connection.cursor()
        cur.execute(drop_view_sql)
        cur.execute(create_view_sql)
        connection.close()

create_gapmider_db= createGapminderDB()
create_gapmider_db.create_database()
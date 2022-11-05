from pip import main

import pandas as pd
import sqlite3

class SystemRs:
    database_rs = None
    diagnosis_code = ""
    tindakan_code = ""
    prediksi = ""
    jumlah = 0

    def loadExcelToDb(self):
        conn = sqlite3.connect("rsdb.db")

        df = pd.read_excel("data.xlsx")
        df.to_sql("data_rs", conn, if_exists="replace")
        conn.execute(
            """
            create table rs_table as
            select * from data_rs
            """
        )
        conn.close()

    def loadDatabse(self):
        conn = sqlite3.connect("rsdb.db")
        df = pd.read_sql_query("SELECT * from rs_table", conn)
        conn.close()
        
        rs = df[
            [
                "NOKARTU",
                "KELAS_RAWAT",
                "SEX",
                "lama dirawat",
                "UMUR_TAHUN",
                "Diagnosis",
                "Tindakan",
                "INACBG",
                "SUBACUTE",
                "CHRONIC",
                "SP",
                "SR",
                "SI",
                "SD",
                "TARIF_INACBG",
                "TARIF_RS",
            ]
        ]

        rs.fillna("-")
        rs["Tindakan"] = rs["Tindakan"].astype(str)
        self.database_rs = rs

    def inputDiagnosisCode(self):
        d1 = input("diagnosis primer")
        d2 = input("diagnosis sekunder 1")
        d3 = input("diagnosis sekunder 2")
        d4 = input("diagnosis sekunder 3")
        input_diagnosis_list = [d1, d2, d3, d4]

        diagnosis_list = []
        for i in input_diagnosis_list:
            if i != "-":
                diagnosis_list.append(i)

        diagnosis_code = ";".join(diagnosis_list)
        if diagnosis_code == "":
            diagnosis_code = "-"

        self.diagnosis_code = diagnosis_code

    def inputTindakanCode(self):
        t1 = input("tindakan primer")
        t2 = input("tindakan sekunder 1")
        t3 = input("tindakan sekunder 2")
        t4 = input("tindakan sekunder 3")
        input_tindakan_list = [t1, t2, t3, t4]

        tindakan_list = []
        for i in input_tindakan_list:
            if i != "-":
                tindakan_list.append(i)

        tindakan_code = ";".join(tindakan_list)
        if tindakan_code == "":
            tindakan_code = "-"

        self.tindakan_code = tindakan_code

    def prediksi(self):
        find = self.database_rs.loc[
            (self.database_rs["Diagnosis"] == self.diagnosis_code)
            & (self.database_rs["Tindakan"] == self.tindakan_code)
        ]

        if find.empty == False:
            tarif_inacbg = find["TARIF_INACBG"].iloc[0]
            tarif_rs = find["TARIF_RS"].sum()
            prediksi = ""
            jumlah = 0

            if tarif_rs > tarif_inacbg:
                prediksi = "untung"
                jumlah = tarif_rs - tarif_inacbg
            else:
                prediksi = "rugi"
                jumlah = tarif_rs - tarif_inacbg

            self.prediksi = prediksi
            self.jumlah = jumlah
            print(self.prediksi)
            print(self.jumlah)


rs = SystemRs()
rs.loadDatabse()
rs.inputDiagnosisCode()
rs.inputTindakanCode()
rs.prediksi()

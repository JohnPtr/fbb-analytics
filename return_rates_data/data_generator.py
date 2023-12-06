import pyodbc
from return_rates_data.config import Config

class DataGenerator():
    @staticmethod
    def test_snowflake_connection():
        print("Testing snowflake connection")
        conn = None
        try:
            print("Connecting...")
            conn = pyodbc.connect("DRIVER=" + Config.SF_DRIVER + "; \
                                   UID=" + Config.SF_UID + "; \
                                   PWD=" + Config.SF_PWD + "; \
                                   SERVER=" + Config.SF_SERVER + "; \
                                   DATABASE=" + Config.SF_DATABASE + "; \
                                   SCHEMA=" + Config.SF_SCHEMA + "; \
                                   WAREHOUSE=" + Config.SF_WAREHOUSE + "; \
                                   ROLE=" + Config.SF_ROLE + ";")
        except Exception as e:
            print(e)
            return None
        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def generate_brand_department_data():
        print("Generating Brand & Department Data")
        conn = None
        try:
            print("Connecting...")
            conn = pyodbc.connect("DRIVER=" + Config.SF_DRIVER + "; \
                                   UID=" + Config.SF_UID + "; \
                                   PWD=" + Config.SF_PWD + "; \
                                   SERVER=" + Config.SF_SERVER + "; \
                                   DATABASE=" + Config.SF_DATABASE + "; \
                                   SCHEMA=" + Config.SF_SCHEMA + "; \
                                   WAREHOUSE=" + Config.SF_WAREHOUSE + "; \
                                   ROLE=" + Config.SF_ROLE + ";")
        except Exception as e:
            print(e)
            return None
        finally:
            if conn is not None:
                delete_query = "DELETE FROM DS_PROJECTS.DS_ANALYTICS_DEV.RETURN_RATES_BRAND_DEPARTMENT_DIM"
                generate_query = "INSERT INTO DS_PROJECTS.DS_ANALYTICS_DEV.RETURN_RATES_BRAND_DEPARTMENT_DIM \
                                with tbl1 as \
                                ( \
                                    SELECT \
                                    b.*, \
                                    case \
                                        when ORDERED_EFFORT = 1 THEN 0 \
                                        when ORDERED_EFFORT = 7 THEN 5 \
                                        when ORDERED_EFFORT = 14 THEN 77 \
                                        ELSE ORDERED_EFFORT \
                                    end AS brand_id, \
                                    CASE WHEN LENGTH(TRIM(DISPOSITION_DATE)) = 10 THEN DISPOSITION_DATE ELSE ORDER_DATE END AS REFDATE \
                                    FROM DS_PROJECTS.DS_ANALYTICS.ORDER_ITEM_HIST_MKTG_VW b \
                                    WHERE \
                                    (LENGTH(TRIM(ORDER_DATE)) = 10  OR LENGTH(TRIM(DISPOSITION_DATE)) = 10 ) \
                                    AND disposition_cd in (0,4) \
                                    AND (TO_DATE(SYSDATE()) -  TO_DATE(ORDER_DATE) BETWEEN 0 AND 730) \
                                    and disposition_cd in (0,4) \
                                ) \
                                , tbl2 AS \
                                ( \
                                    SELECT  a.ORDERED_EFFORT, a.brand_id, a.department, b.department_name, \
                                    MIN(a.REFDATE) AS MIN_REFDATE, \
                                    MAX(a.REFDATE) AS MAX_REFDATE \
                                    FROM tbl1 a \
                                    LEFT JOIN DS_PROJECTS.PRODUCT_DATA_MODEL.DEPARTMENT b on a.brand_id = b.brand_id AND a.department = b.department_id \
                                    group by a.ORDERED_EFFORT, a.brand_id, a.department, b.department_name \
                                ) \
                                SELECT a.ORDERED_EFFORT, brand_id, \
                                CASE \
                                        WHEN a.BRAND_ID = 0 THEN 'Woman Within (1)' \
                                        WHEN a.BRAND_ID = 5 THEN 'Roaman''s (7)' \
                                        WHEN a.BRAND_ID = 11 THEN 'King size (11)' \
                                        WHEN a.BRAND_ID = 26 THEN 'Catherine''s (26)' \
                                        WHEN a.BRAND_ID = 27 THEN 'Eloquii (27)' \
                                        WHEN a.BRAND_ID = 15 THEN 'Brylane Home (15)' \
                                        WHEN a.BRAND_ID = 24 THEN 'Swimsuits For All (24)' \
                                        WHEN a.BRAND_ID = 23 THEN 'Jessica London (23)' \
                                        WHEN a.BRAND_ID = 25 THEN 'Ellos (25)' \
                                        WHEN a.BRAND_ID = 28 THEN 'CP (28)' \
                                        WHEN a.BRAND_ID = 20 THEN 'OSP (20)' \
                                        ELSE 'Other (' || a.BRAND_ID || ')' \
                                    END AS brand_name, \
                                department as department_id, \
                                department_name, \
                                CASE \
                                    WHEN department_name IS NULL THEN department || '/NA' \
                                    ELSE department || '/' || department_name \
                                END as department_name_shiny, \
                                min_refdate, \
                                max_refdate \
                                FROM tbl2 A"

                query_issue = False
                try:
                    cursor = conn.cursor()
                    cursor.execute(delete_query)
                    cursor.execute(generate_query)
                except Exception as e:
                    query_issue = True
                    print(e)
                finally:
                    if not query_issue:
                        conn.commit()

                conn.close()
                print("Connection closed.")

    @staticmethod
    def generate_brand_department_style_data():
        print("Generating Brand, Department & Style Data")
        conn = None
        try:
            print("Connecting...")
            conn = pyodbc.connect("DRIVER=" + Config.SF_DRIVER + "; \
                                   UID=" + Config.SF_UID + "; \
                                   PWD=" + Config.SF_PWD + "; \
                                   SERVER=" + Config.SF_SERVER + "; \
                                   DATABASE=" + Config.SF_DATABASE + "; \
                                   SCHEMA=" + Config.SF_SCHEMA + "; \
                                   WAREHOUSE=" + Config.SF_WAREHOUSE + "; \
                                   ROLE=" + Config.SF_ROLE + ";")
        except Exception as e:
            print(e)
            return None
        finally:
            if conn is not None:
                delete_query = "DELETE FROM DS_PROJECTS.DS_ANALYTICS_DEV.RETURN_RATES_BRAND_DEPARTMENT_STYLE_DIM"
                generate_query = "INSERT INTO DS_PROJECTS.DS_ANALYTICS_DEV.RETURN_RATES_BRAND_DEPARTMENT_STYLE_DIM \
                                 select distinct ORDERED_EFFORT as BRAND_ID, department AS DEPARTMENT_ID, ordered_style AS SHIPPED_STYLE \
                                 FROM DS_PROJECTS.DS_ANALYTICS.ORDER_ITEM_HIST_MKTG_VW b \
                                    WHERE \
                                    (LENGTH(TRIM(ORDER_DATE)) = 10  OR LENGTH(TRIM(DISPOSITION_DATE)) = 10 ) \
                                    AND disposition_cd in (0,4) \
                                    AND (TO_DATE(SYSDATE()) -  TO_DATE(ORDER_DATE) BETWEEN 0 AND 730) \
                                    and disposition_cd in (0,4)"

                query_issue = False
                try:
                    cursor = conn.cursor()
                    cursor.execute(delete_query)
                    cursor.execute(generate_query)
                except Exception as e:
                    query_issue = True
                    print(e)
                finally:
                    if not query_issue:
                        conn.commit()

                conn.close()
                print("Connection closed.")

    @staticmethod
    def generate_brand_department_style_product_data():
        print("Generating Brand, Department, Style & Product Data")
        conn = None
        try:
            print("Connecting...")
            conn = pyodbc.connect("DRIVER=" + Config.SF_DRIVER + "; \
                                   UID=" + Config.SF_UID + "; \
                                   PWD=" + Config.SF_PWD + "; \
                                   SERVER=" + Config.SF_SERVER + "; \
                                   DATABASE=" + Config.SF_DATABASE + "; \
                                   SCHEMA=" + Config.SF_SCHEMA + "; \
                                   WAREHOUSE=" + Config.SF_WAREHOUSE + "; \
                                   ROLE=" + Config.SF_ROLE + ";")
        except Exception as e:
            print(e)
            return None
        finally:
            if conn is not None:
                delete_query = "DELETE FROM DS_PROJECTS.DS_ANALYTICS_DEV.RETURN_RATES_BRAND_DEPARTMENT_STYLE_PRODUCT_DIM"
                generate_query = "INSERT INTO DS_PROJECTS.DS_ANALYTICS_DEV.RETURN_RATES_BRAND_DEPARTMENT_STYLE_PRODUCT_DIM \
                                select distinct ORDERED_EFFORT as BRAND_ID, department AS DEPARTMENT_ID, ordered_style AS SHIPPED_STYLE, MERCH_ITEM_NUM as SHIPPED_PRODUCT \
                                FROM DS_PROJECTS.DS_ANALYTICS.ORDER_ITEM_HIST_MKTG_VW b \
                                    WHERE \
                                    (LENGTH(TRIM(ORDER_DATE)) = 10  OR LENGTH(TRIM(DISPOSITION_DATE)) = 10 ) \
                                    AND disposition_cd in (0,4) \
                                    AND (TO_DATE(SYSDATE()) -  TO_DATE(ORDER_DATE) BETWEEN 0 AND 730) \
                                    and disposition_cd in (0,4)"

                query_issue = False
                try:
                    cursor = conn.cursor()
                    cursor.execute(delete_query)
                    cursor.execute(generate_query)
                except Exception as e:
                    query_issue = True
                    print(e)
                finally:
                    if not query_issue:
                        conn.commit()

                conn.close()
                print("Connection closed.")

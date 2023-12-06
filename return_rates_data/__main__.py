import fire

from return_rates_data.data_generator import DataGenerator

class CLI:
    @staticmethod
    def update_data():
        # DataGenerator.test_snowflake_connection()
        DataGenerator.generate_brand_department_data()
        DataGenerator.generate_brand_department_style_data()
        DataGenerator.generate_brand_department_style_product_data()

def main():
    fire.Fire(CLI)


if __name__ == "__main__":
    main()

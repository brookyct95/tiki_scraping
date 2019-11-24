import Utilities
import Category

Utilities.create_category_table()
#Utilities.create_products_table()

main_cat = Category.get_main_categories(save_db = True)
Category.get_all_sub_categories(main_cat[1])
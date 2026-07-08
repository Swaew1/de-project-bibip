from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
import os 
from decimal import Decimal 

class CarService:
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        # 1. Задаем пути к файлам прямо здесь
        models_file = self.root_directory_path + "/models.txt"
        index_file = self.root_directory_path + "/models_index.txt"

        line_count = 0
        if os.path.exists(index_file):
            with open(index_file, "r") as f:
                line_count = len(f.readlines())

        raw_text = f"{model.id};{model.name};{model.brand}"
        formatted_row = raw_text.ljust(500) + "\n"
        
        mode = "r+" if os.path.exists(models_file) else "w+"
        with open(models_file, mode) as f:
            f.seek(line_count * 501)
            f.write(formatted_row)
            
        with open(index_file, "a") as f:
            f.write(f"{model.id},{line_count}\n")
            
        return model

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:

        cars_file = self.root_directory_path + '/cars.txt'
        index_file = self.root_directory_path + '/cars_index.txt'

        line_count = 0
        if os.path.exists(index_file):
            with open(index_file, 'r') as f: 
                line_count = len(f.readlines())

        raw_text = f"{car.vin};{car.model};{car.price};{car.date_start};{car.status.value}"
        formatted_row = raw_text.ljust(500) + '\n'

        mode = 'r+' if os.path.exists(cars_file) else 'w+'
        with open(cars_file, mode) as f:
            f.seek(line_count * 501)
            f.write(formatted_row)

        with open(index_file, 'a') as f:
            f.write(f'{car.vin},{line_count}\n')

        return car

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        sale_file = self.root_directory_path + '/sales.txt'
        index_file = self.root_directory_path + '/sales_index.txt'
        cars_file = self.root_directory_path + '/cars.txt'
        cars_index_file = self.root_directory_path + '/cars_index.txt'

    
        car_line_number = 0
        with open(cars_index_file, 'r') as f:
            for line in f:
                if line.strip():
                    vin_key, line_num = line.strip().split(',')
                    if vin_key == sale.car_vin:
                        car_line_number = int(line_num)
                        break

        with open(cars_file, 'r') as f:
            f.seek(car_line_number * 501)
            car_row = f.read(500).strip()

        car_fields = car_row.split(';')
        car_fields[4] = 'sold'
        new_raw_text = ";".join(car_fields)
        new_formatted_row = new_raw_text.ljust(500) + "\n"

        with open(cars_file, 'r+') as f:
            f.seek(car_line_number * 501)
            f.write(new_formatted_row)

        line_count = 0
        if os.path.exists(index_file):
            with open(index_file, 'r') as f: 
                line_count = len(f.readlines())

        raw_text = f'{sale.sales_number};{sale.car_vin};{sale.sales_date};{sale.cost}'
        formatted_row = raw_text.ljust(500) + '\n'

        mode = 'r+' if os.path.exists(sale_file) else 'w+'
        with open(sale_file, mode) as f:
            f.seek(line_count * 501)
            f.write(formatted_row)

        with open(index_file, 'a') as f:
            f.write(f'{sale.car_vin},{line_count}\n')

        return Car(
            vin=car_fields[0],
            model=int(car_fields[1]),
            price=Decimal(car_fields[2]),
            date_start=car_fields[3],
            status=CarStatus.sold
        )
        

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        cars_file = self.root_directory_path + '/cars.txt'
        result = []
        
        if not os.path.exists(cars_file):
            return result
            
        with open(cars_file, 'r') as f:
            while True:
                line = f.read(501)
                if not line:
                    break
                    
                clean_line = line.strip()
                if not clean_line:
                    continue
                    
                fields = clean_line.split(';')

                if fields[4] == status.value:
                    result.append(Car(
                        vin=fields[0],
                        model=int(fields[1]),
                        price=Decimal(fields[2]),
                        date_start=fields[3],
                        status=CarStatus(fields[4])
                    ))
                    
        return result              

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        car_line_number = None 
        cars_index_file = self.root_directory_path + '/cars_index.txt'

        if os.path.exists(cars_index_file):
            with open(cars_index_file, 'r') as f:
                for line in f:
                    if line.strip():
                        vin_key, line_num = line.strip().split(',')
                        if vin_key == vin:
                            car_line_number = int(line_num)
                            break 

        if car_line_number is None:
            return None 

        cars_file = self.root_directory_path + '/cars.txt' 
        with open(cars_file, 'r') as f:
            f.seek(car_line_number * 501)
            car_row = f.read(500).strip()

        car_fields = car_row.split(';')

        model_id = car_fields[1]
        model_line_number = None 
        models_index_file = self.root_directory_path + '/models_index.txt'

        with open(models_index_file, 'r') as f:
            for line in f:
                if line.strip():
                    m_id, line_num = line.strip().split(',')
                    if m_id == model_id:
                        model_line_number = int(line_num)
                        break

        models_file = self.root_directory_path + '/models.txt'
        with open(models_file, 'r') as f:
            f.seek(model_line_number * 501)
            model_row = f.read(500).strip()

        model_fields = model_row.split(';')

        sales_date = None
        sales_cost = None

        if car_fields[4] == 'sold':
            sales_index_file = self.root_directory_path + '/sales_index.txt'
            sale_line_number = None
        
            if os.path.exists(sales_index_file):
                with open(sales_index_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            v_key, line_num = line.strip().split(',')
                            if v_key == vin:
                                sale_line_number = int(line_num)
                                break
                            
            if sale_line_number is not None:
                sales_file = self.root_directory_path + '/sales.txt'
                with open(sales_file, 'r') as f:
                    f.seek(sale_line_number * 501)
                    sale_row = f.read(500).strip()
            
                sale_fields = sale_row.split(';')
                sales_date = sale_fields[2]
                sales_cost = Decimal(sale_fields[3])

        return CarFullInfo(
            vin=car_fields[0],
            car_model_name=model_fields[1],
            car_model_brand=model_fields[2],
            price=Decimal(car_fields[2]),
            date_start=car_fields[3],
            status=CarStatus(car_fields[4]),
            sales_date=sales_date,
            sales_cost=sales_cost
        )

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        cars_index_file = self.root_directory_path + '/cars_index.txt' 
        cars_file = self.root_directory_path + '/cars.txt' 

        cars_index = {}
        if os.path.exists(cars_index_file):
            with open(cars_index_file, 'r') as f:
                for line in f:
                    if line.strip():
                        v_key, line_num = line.strip().split(',')
                        cars_index[v_key] = int(line_num)
                        
        if vin not in cars_index:
            raise ValueError('Машина со старым VIN не найдена')
        if new_vin in cars_index:
            raise ValueError('Машина с новым VIN уже существует в базе')

        car_line_number = cars_index[vin]

        with open(cars_file, 'r') as f:
            f.seek(car_line_number * 501)
            car_row = f.read(500).strip()

        car_fields = car_row.split(';')
        car_fields[0] = new_vin

        new_raw_text = ';'.join(car_fields)
        new_formatted_row = new_raw_text.ljust(500) + '\n'

        with open(cars_file, 'r+') as f:
            f.seek(car_line_number * 501)
            f.write(new_formatted_row)

        del cars_index[vin]
        cars_index[new_vin] = car_line_number

        with open(cars_index_file, 'w') as f:
            for v_key, line_num in cars_index.items():
                f.write(f'{v_key},{line_num}\n')

        return Car(
            vin=car_fields[0],
            model=int(car_fields[1]), 
            price=Decimal(car_fields[2]),
            date_start=car_fields[3], 
            status=CarStatus(car_fields[4])
        )

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> None:
        sales_file = self.root_directory_path + '/sales.txt'
        sales_index_file = self.root_directory_path + '/sales_index.txt'
        
        target_vin = None
        sale_line_number = None

        if os.path.exists(sales_file):
            with open(sales_file, 'r', encoding='utf-8') as f:
                for idx, line in enumerate(f):
                    clean_line = line.strip()
                    if not clean_line:
                        continue
                    sale_fields = clean_line.split(';')
                    if sale_fields[0] == sales_number:
                        target_vin = sale_fields[1]
                        sale_line_number = idx
                        break

        if target_vin is None:
            return

        cars_index_file = self.root_directory_path + '/cars_index.txt'
        cars_file = self.root_directory_path + '/cars.txt'
        car_line_number = None

        if os.path.exists(cars_index_file):
            with open(cars_index_file, 'r') as f:
                for line in f:
                    if line.strip():
                        vin_key, line_num = line.strip().split(',')
                        if vin_key == target_vin:
                            car_line_number = int(line_num)
                            break

        if car_line_number is not None:
            with open(cars_file, 'r') as f:
                f.seek(car_line_number * 501)
                car_row = f.read(500).strip()
            
            car_fields = car_row.split(';')
            car_fields[4] = 'available'
            
            new_car_row = ";".join(car_fields).ljust(500) + "\n"
            with open(cars_file, 'r+') as f:
                f.seek(car_line_number * 501)
                f.write(new_car_row)

        sales_index = {}
        if os.path.exists(sales_index_file):
            with open(sales_index_file, 'r') as f:
                for line in f:
                    if line.strip():
                        v_key, line_num = line.strip().split(',')
                        sales_index[v_key] = int(line_num)

        if target_vin in sales_index:
            del sales_index[target_vin]

        with open(sales_index_file, 'w') as f:
            for v_key, line_num in sales_index.items():
                f.write(f'{v_key},{line_num}\n')

        if sale_line_number is not None:
            empty_row = "".ljust(500) + "\n"
            with open(sales_file, 'r+') as f:
                f.seek(sale_line_number * 501)
                f.write(empty_row)
        

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        sales_file = self.root_directory_path + '/sales.txt'
        cars_index_file = self.root_directory_path + '/cars_index.txt'
        cars_file = self.root_directory_path + '/cars.txt'
        
        stats = {}

        if os.path.exists(sales_file):
            cars_data = {}
            if os.path.exists(cars_index_file) and os.path.exists(cars_file):
                with open(cars_index_file, 'r') as f:
                    cars_index = {line.strip().split(',')[0]: int(line.strip().split(',')[1]) for line in f if line.strip()}
                
                with open(cars_file, 'r') as f:
                    for vin, line_num in cars_index.items():
                        f.seek(line_num * 501)
                        fields = f.read(500).strip().split(';')
                        if len(fields) >= 3:
                            cars_data[vin] = (fields[1], Decimal(fields[2]))

            with open(sales_file, 'r', encoding='utf-8') as f:
                for line in f:
                    clean_line = line.strip()
                    if not clean_line:
                        continue
                    sale_fields = clean_line.split(';')
                    vin = sale_fields[1]
                    
                    if vin in cars_data:
                        model_id, price = cars_data[vin]
                        if model_id not in stats:
                            stats[model_id] = {"count": 0, "max_price": Decimal('0')}
                        stats[model_id]["count"] += 1
                        if price > stats[model_id]["max_price"]:
                            stats[model_id]["max_price"] = price

        sorted_stats = sorted(
            stats.items(), 
            key=lambda item: (-item[1]["count"], -item[1]["max_price"])
        )
        top_3 = sorted_stats[:3]

        models_index_file = self.root_directory_path + '/models_index.txt'
        models_file = self.root_directory_path + '/models.txt'
        
        models_index = {}
        if os.path.exists(models_index_file):
            with open(models_index_file, 'r') as f:
                for line in f:
                    if line.strip():
                        m_id, line_num = line.strip().split(',')
                        models_index[m_id] = int(line_num)

        result = []
        for model_id, info in top_3:
            if model_id in models_index:
                line_num = models_index[model_id]
                with open(models_file, 'r') as f:
                    f.seek(line_num * 501)
                    model_fields = f.read(500).strip().split(';')
                
                stats_obj = ModelSaleStats(
                    car_model_name=model_fields[1],
                    brand=model_fields[2],
                    sales_number=info["count"]
                )
                result.append(stats_obj)

        return result

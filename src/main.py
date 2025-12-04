import flet as ft



class GenericCard(ft.Container):
    def __init__(self):
        super().__init__()
        self.border_radius = ft.border_radius.all(15)
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            offset=ft.Offset(0, 5)
        )
        self.bgcolor = "#A935B9"
        self.expand=True
        self.expand_loose = True
        self.padding = 15
        self.content = ft.Text("Gestor de gastos",color = "#C5EDAC",size=32,weight=ft.FontWeight.BOLD)
        

        

class SalaryContent(GenericCard):
    def __init__(self,func):
        super().__init__()
        self.field = ft.TextField(bgcolor=ft.Colors.WHITE)
        salario = ft.Column([ft.Text("Salario Mensual",weight=ft.FontWeight.BOLD,size=26,color=ft.Colors.WHITE),self.field],tight=True,horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.content = salario
        self.height = 150
        self.field.on_change = func



class SpensesContent(GenericCard):
    def __init__(self,func):
        super().__init__()
        
        self.spense_name = ft.TextField(label="Nombre de Gasto",bgcolor=ft.Colors.WHITE)
        self.spense_value = ft.TextField(label="costo",bgcolor=ft.Colors.WHITE,input_filter=ft.NumbersOnlyInputFilter())
        lowls = ft.Row([self.spense_name,self.spense_value])
        self.content = ft.Column([ft.Text("Agregar nuevos gastos",color=ft.Colors.WHITE,size=26,weight=ft.FontWeight.BOLD),lowls,ft.ElevatedButton("Agregar Gasto",on_click=func)],tight=True,horizontal_alignment=ft.CrossAxisAlignment.CENTER)

class SpenseCard(GenericCard):
    def __init__(self,nombre,valor,func):
        super().__init__()
        self.bgcolor="#7A918D"
        self.valor = valor
        self.spense_name = ft.Text(nombre,color=ft.Colors.WHITE,size=22)
        self.spense_value = ft.Text("$"+str(self.valor),color=ft.Colors.RED,size=22)
        self.content = ft.Row([self.spense_name,self.spense_value,ft.IconButton(icon=ft.Icons.DELETE,on_click=lambda e: func(self))],tight=True,alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        



class SpensesList(GenericCard):
    def __init__(self):
        super().__init__()
        self.list = ft.ListView(auto_scroll=True,expand=True)
        self.total = ft.Text(f"Total sobrante: 0",color = ft.Colors.GREEN,size=30,weight=ft.FontWeight.BOLD)
        column = ft.Column([ft.Text("Lista de Gastos",color = "#C5EDAC",weight=ft.FontWeight.BOLD,size=32),self.list,self.total],expand=True)
        self.expand=True
        self.content = column
    
    def new_total(self,new):
        self.total.value = f"Total sobrante: ${new}"
        if new < 0:
            self.total.color = ft.Colors.RED
        else:
            self.total.color = ft.Colors.GREEN

class App:
    def __init__(self,page: ft.Page):
        self.salary = 0
        self.page = page
        self.page.window.width = 720
        self.page.window.height = 1280
        self.page.bgcolor = "#C5EDAC"
        self.page.adaptive = True
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        

        self.salaryContent = SalaryContent(self.new_salary)
        self.spensesContent = SpensesContent(self.add_spense)
        self.spensesList = SpensesList()

        for i in self.page.client_storage.get_keys(""):
            valor = self.page.client_storage.get(i)
            self.spensesList.list.controls.append(SpenseCard(i,valor,self.delete_spense))
        self.setup_ui()

    def setup_ui(self):
        self.page.add(
            ft.Column([
                GenericCard(),
                self.salaryContent,
                self.spensesContent,
                self.spensesList
            ],expand=True,auto_scroll=True,alignment=ft.MainAxisAlignment.START
            )
            
        )

    def add_spense(self,e):
        self.spensesList.list.controls.append(SpenseCard(self.spensesContent.spense_name.value,self.spensesContent.spense_value.value,self.delete_spense))
        self.calculate_spenses()
        self.page.client_storage.set(self.spensesContent.spense_name.value,float(self.spensesContent.spense_value.value))
        self.page.update()
    
    def new_salary(self,e):
        
        self.salary = float(self.salaryContent.field.value)
        
        self.calculate_spenses()
        self.page.update()

    def delete_spense(self,e):
        self.spensesList.list.controls.remove(e)
        self.page.client_storage.remove(e.spense_name.value)
        self.calculate_spenses()
        self.page.update()

    def calculate_spenses(self):
        sal = self.salary
        for i in self.spensesList.list.controls:
            sal -= float(i.valor)
        self.spensesList.new_total(sal)
        self.page.update()

def main(page: ft.Page):
    App(page)


ft.app(main)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton

from entity.cliente import Cliente
from repository.cliente_repositorio import ClienteRepositorio


class BotaoListagem(ToggleButton):
    def __init__(self, cliente_id, cliente_nome, cliente_idade, **kwargs):
        super(BotaoListagem, self).__init__(**kwargs)
        self.id_cliente = cliente_id
        self.nome_cliente = cliente_nome
        self.idade_cliente = cliente_idade
        self.text = self.nome_cliente + " " + self.idade_cliente
        self.group = 'clientes'


class Principal(BoxLayout):
    def __init__(self, **kwargs):
        super(Principal, self).__init__(**kwargs)
        self.listar_clientes()

    def cadastrar_cliente(self):
        try:
            nome = self.ids.nome.text
            idade = int(self.ids.idade.text)

            cliente = Cliente(nome, idade)
            ClienteRepositorio.inserir_cliente(cliente)
            self.listar_clientes()

            self.ids.nome.text = ''
            self.ids.idade.text = ''

            self.ids.box_layout_erro.height = "0dp"
            self.ids.label_erro.text = ""


        except ValueError as ve:
            self.ids.box_layout_erro.height = "40dp"
            self.ids.label_erro.text = f"Erro: {ve}"

    def listar_clientes(self):
        self.ids.clientes.clear_widgets()
        clientes = ClienteRepositorio.listar_clientes()
        for i in clientes:
            id = str(i[0])
            nome = i[1]
            idade = str(i[2])
            self.ids.clientes.add_widget(BotaoListagem(id, nome, idade))


class Crud(App):
    def build(self):
        return Principal()


Crud().run()

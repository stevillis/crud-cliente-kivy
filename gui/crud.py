from kivy.app import App
from kivy.properties import partial
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton

from entity.cliente import Cliente
from repository.cliente_repositorio import ClienteRepositorio


class ExclusaoPopup(Popup):
    pass


class BotaoListagem(ToggleButton):
    def __init__(self, cliente_id, cliente_nome, cliente_idade, **kwargs):
        super(BotaoListagem, self).__init__(**kwargs)
        self.id_cliente = cliente_id
        self.nome_cliente = cliente_nome
        self.idade_cliente = cliente_idade
        self.text = self.nome_cliente + " " + self.idade_cliente
        self.group = 'clientes'

    def _do_release(self, *args):
        Principal().cliente_selecionado(self.id_cliente)


class Principal(BoxLayout):
    id_cliente = 0

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

    def cliente_selecionado(self, id):
        Principal.id_cliente = id

    def remover(self, id):
        ClienteRepositorio.remover_cliente(id)
        self.listar_clientes()

    def editar_cliente(self):
        try:
            id = Principal.id_cliente

            nome = self.ids.nome.text
            idade = int(self.ids.idade.text)

            cliente = Cliente(nome, idade)
            ClienteRepositorio.editar_cliente(id, cliente)
            self.listar_clientes()

            self.ids.nome.text = ''
            self.ids.idade.text = ''
        except ValueError as ve:
            self.ids.box_layout_erro.height = "40dp"
            self.ids.label_erro.text = f"Erro: {ve}"

    def remover_cliente(self):
        id = Principal.id_cliente

        try:
            if int(id) > 0:
                popup = ExclusaoPopup()
                popup.title = "Excluir Cliente"
                popup.funcao = partial(self.remover, id)
                popup.open()
            else:
                self.ids.box_layout_erro.height = "40dp"
                self.ids.label_erro.text = f"Atenção: Selecione um Cliente antes de remover!"
        except TypeError as te:
            self.ids.box_layout_erro.height = "40dp"
            self.ids.label_erro.text = f"Erro: {te}"


class Crud(App):
    def build(self):
        return Principal()


Crud().run()

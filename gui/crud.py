from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from entity.cliente import Cliente
from repository.cliente_repositorio import ClienteRepositorio


class Principal(BoxLayout):
    def cadastrar_cliente(self):
        nome = self.ids.nome.text
        idade = int(self.ids.idade.text)

        if len(nome) > 0 and idade > 0:
            cliente = Cliente(nome, idade)
            ClienteRepositorio.inserir_cliente(cliente)

        self.ids.nome.text = ''
        self.ids.idade.text = ''


class Crud(App):
    def build(self):
        return Principal()


Crud().run()

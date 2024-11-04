

from flask import Flask, render_template, redirect, request, flash
import json
import ast


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ECOKIDS'

logado = False

@app.route('/')
def home():
    global logado
    logado = False
    return render_template('login.html')


@app.route('/adm')
def adm():
    if logado == True:
        with open('usuarios.json') as usuariosTemp:
            usuario = json.load(usuariosTemp)
            usuario =[]
        return render_template("administrador.html",usuario=usuario)  
    if logado == False:
        return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    global logado
    nome = request.form.get('nome')
    senha = request.form.get('senha')    
   
    with open('usuarios.json') as usuariosTemp:
          usuario = json.load(usuariosTemp)
          cont = 0
          for usuario in usuario:
                cont += 1

                if nome == 'adm' and senha=='000':
                    logado = True
                    return redirect('/adm')
                
                if usuario['nome']==nome and usuario['senha']==senha:
                    return render_template("usuarios.html")
                
                if cont >= len(usuario):
                    flash('USUARIO INVALIDO')
                    return redirect("/")
  

@app.route('/cadastrarUsuario', methods=['POST'] )
def cadastrarUsuario():
    user:[] # type: ignore
    nome = request.form.get('nome')
    senha = request.form.get('senha')    
    user[
        {
             "nome": nome,
             "senha": senha
        }
    ]
    with open('usuarios.json') as usuariosTemp:
          usuario = json.load(usuariosTemp)

    usuarioNovo= usuario + user

    with open('usuarios.json', 'w') as gravarTemp:
       json.dump(usuarioNovo, gravarTemp, indent=4 )
    logado = True    
    return redirect('/adm')


@app.route('/excluirUsuario', methods= ['POST'])
def excluirUsuario():
    global logado
    logado = True
    usuario = request.form.get('usuarioPexcluir')
    usuarioDict = ast.literal_eval(usuario)
    nome = usuarioDict ['nome']
    with open('usuario.json') as usuariosTemp:
        usuarioJson = json.load(usuariosTemp)
        for c in usuarioJson:
            if c == usuarioDict:
                usuarioJson.remove(usuarioDict)
                with open('usuario.json', 'w') as usuarioPexcluir:
                    json.dump(usuarioJson, usuarioPexcluir, indent=4)


    return redirect('/adm')



if __name__ in '__main__':
      app.run(debug=True)
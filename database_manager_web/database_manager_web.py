from flask import Flask, render_template, request, redirect
import database
import database_tools
app = Flask(__name__)

games = database.search_roms_by_name("")

def refresh_games():
   global games
   games = database.search_roms_by_name("")



@app.route('/', methods=['GET', 'POST'])
def search():
   systems = database_tools.systems.copy()
   systems.insert(0,"")
   return render_template('search.html', data=games,systems=systems)


@app.route('/new', methods=['GET'])
def new():
   status = {}
   rom = {}
   rom['uuid'] = database_tools.generate_uuid()
   rom["release_name"] = ""
   rom["region"] = ""
   rom["system"] = ""
   rom['sha1'] = ""
   rom["rom_extensionless_file_name"] = ""
   rom["publisher"] = ""
   rom["date"] = ""
   rom["developer"] = ""
   rom["genre"] = ""
   rom["description"] = ""
   rom["reference_url"] = ""
   rom["manual_url"] = ""
   return render_template('view.html', data=rom,status=status,systems=database_tools.systems)


@app.route('/view', methods=['POST'])
def view():
    status = {}
    data = database.get_rom_by_uuid(request.form['uuid'])
    return render_template('view.html', data=data,status=status,systems=database_tools.systems)

@app.route('/delete', methods=['POST'])
def delete():
    database.delete_rom(request.form["uuid"])
    refresh_games()
    return redirect("/", code=302)

@app.route('/edit', methods=['POST'])
def edit():
   form = request.form.copy()
   form['uuid'] = form['uuid'].upper()
   status = {}
   if request.form["duplicate"] == "true":
         form["uuid"] = database_tools.generate_uuid()
         form['duplicate'] = "false"
         status["message"] = "You are now editing a duplicated rom"
         return render_template('view.html', data=form,status=status,systems=database_tools.systems)

   rom = database.get_rom_by_uuid(request.form["uuid"])
   # rom already exist so we will update
   if len(rom) > 0:
      database.update_rom(request.form)
      refresh_games()
      return redirect("/", code=302)
   else:
      if database.is_new_rom(request.form):
         database.update_rom(request.form)
         refresh_games()      
         return redirect("/", code=302)
      else:
         status["message"] = "Either Sha1 or Rom Extensionless File Name need to be unique"
         return render_template('view.html', data=request.form,status=status,systems=database_tools.systems)
   


if __name__ == '__main__':
    app.debug = True
    app.run()

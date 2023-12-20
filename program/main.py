from flask import (Flask, 
                    render_template, 
                    request, 
                    flash, 
                    redirect, 
                    url_for, 
                    jsonify,
                    make_response)


from .solve_algorithms import SimplexMethod, EvolutionAlgorithm

app = Flask(__name__)
app.config["SECRET_KEY"] = "sjdFODJdsojfsodfjPFJdjs546sdfsoidfjPfj"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/evolution_solve", methods=["POST"])
def evolution_solve():
    if request.method == "POST":
        response = { 'ok': True, 'html': None }
        
        data = request.get_json()
        form_data = data.get('formData')

        try:
            form_data = format_form_data_evolution(form_data)
        except:
            response["ok"] = False
            response['html'] = render_template('error_message.html', 
                                               messages=["Ошибка!", "Проверьте коррестность введенных данных!"])
            return jsonify(response)
        if form_data["populationSize"] <= form_data["tournamentSize"]:
            response["ok"] = False
            response['html'] = render_template('error_message.html', 
                                               messages=["Ошибка!", "Выборка особей не может быть >= количеству особей в популяции!"])
            return jsonify(response)

        method = EvolutionAlgorithm(
            profits=form_data["profits"],
            constraints=form_data["tableData"],
            reserves=form_data["reserves"],
            population_size=form_data["populationSize"],
            bounds=[form_data["minArgVal"], form_data["maxArgVal"]],
            num_generations=form_data["numGenerations"],
            mutation_rate=form_data["mutationRate"],
            tournament_size=form_data["tournamentSize"]
        )
        response['html'] = render_template('evolution_solution.html', solution=method.solution) 
        return jsonify(response)
        

@app.route("/simplex_solve", methods=["POST"])
def read_table():
    if request.method == "POST":
        response = { 'ok': True, 'html': None }
        
        data = request.get_json()
        form_data = data.get('formData')

        try:
            form_data = format_form_data_simplex(form_data)
        except:
            response["ok"] = False
            response['html'] = render_template('error_message.html', 
                                               messages=["Ошибка!", "Проверьте коррестность введенных данных!"])
            return jsonify(response)

        method = SimplexMethod(materials=form_data["tableData"],
                               reserve=form_data["reserves"],
                               profit=form_data["profits"])


        response['html'] = render_template('simplex_solution.html', solution=method.solution)
        return jsonify(response)
    

def format_form_data_simplex(form_data: dict):
    form_data["tableData"] = [[float(el) for el in row] for row in form_data["tableData"]]
    form_data["reserves"] = [float(res) for res in form_data["reserves"]]
    form_data["profits"] = [float(prof) for prof in form_data["profits"]]
    return form_data


def format_form_data_evolution(form_data: dict):
    form_data["populationSize"] = int(form_data["populationSize"])
    form_data["numGenerations"] = int(form_data["numGenerations"])
    form_data["mutationRate"] = float(form_data["mutationRate"]) / 100
    form_data["tournamentSize"] = int(form_data["tournamentSize"])
    form_data["minArgVal"] = int(form_data["minArgVal"])
    form_data["maxArgVal"] = int(form_data["maxArgVal"])
    form_data.update(format_form_data_simplex(form_data))
    return form_data


if __name__ == "__main__":
    app.run()

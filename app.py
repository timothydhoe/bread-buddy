from flask import Flask, render_template, request
import bakers_calculators as bc

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    """Homepage"""
    # return render_template('index.html')

    """Baker's percentage calculator"""
    result = None
    error = None

    if request.method == 'POST':
        try:
            # Get form data
            flour_weight = float(request.form.get('flour_weight'))
            water_ratio = float(request.form.get('water_ratio')) / 100
            salt_ratio = float(request.form.get('salt_ratio')) / 100
            levain_ratio = float(request.form.get('levain_ratio')) / 100
            
            # Build formula
            formula = {
                "water_weight": water_ratio,
                "salt_weight": salt_ratio,
                "levain_weight": levain_ratio
            }
            
            # Calculate
            result = bc.bakers_percentage(flour_weight, formula)
            
        except (ValueError, TypeError) as e:
            error = str(e)
        
    return render_template('index.html', result=result, error=error)


# @app.route('/bakers-percentage', methods=['GET', 'POST'])
# def bakers_percentage():

    
#     return render_template('bakers_percentage.html', result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True)
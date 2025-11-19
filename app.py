from flask import Flask, render_template, request
import bakers_calculators as bc

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    """Homepage"""
    # return render_template('index.html')

    """Baker's percentage calculator"""
    result = None
    hydration_result = None
    water_temp_result = None
    fermentation_result = None  
    error = None

    if request.method == 'POST':
        try:
            # Get form data
            flour_weight = float(request.form.get('flour_weight'))
            water_ratio = float(request.form.get('water_ratio')) / 100
            salt_ratio = float(request.form.get('salt_ratio')) / 100
            levain_ratio = float(request.form.get('levain_ratio')) / 100
            scale_factor = float(request.form.get('scale_factor', 1))
            
            # Additional settings
            ambient_temp = float(request.form.get('ambient_temp', 22))
            target_dough_temp = float(request.form.get('target_dough_temp', 25))
            base_fermentation = float(request.form.get('base_fermentation', 4))
            
            # Build formula
            formula = {
                "water_weight": water_ratio,
                "salt_weight": salt_ratio,
                "levain_weight": levain_ratio
            }
            
            # Calculate
            result = bc.bakers_percentage(flour_weight, formula)
            hydration_result = bc.calculate_hydration(
                result['flour_weight'], 
                result['water_weight']
            )

            # Scaling happens here
            if scale_factor != 1:
                result = bc.recipe_scaler(scale_factor, result)



            # Water temp using target_dough_temp
            water_temp_result = bc.mixing_water_temperature(
            ddt=target_dough_temp,
            ambient_temp=ambient_temp
        )

            # Bulk fermentation using base_fermentation
            fermentation_result = bc.bulk_fermentation_adjuster(
            base_fermentation, 
            ambient_temp=ambient_temp
        )

        except (ValueError, TypeError) as e:
            error = str(e)
        
    return render_template('index.html',
                        result=result,
                        hydration_result=hydration_result,
                        water_temp_result=water_temp_result,
                        fermentation_result=fermentation_result,
                        error=error)

# @app.route('/bakers-percentage', methods=['GET', 'POST'])
# def bakers_percentage():

    
#     return render_template('bakers_percentage.html', result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True)
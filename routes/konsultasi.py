from flask import Blueprint, render_template, request
from core.expert_system.engine import get_expert_analysis

konsultasi_bp = Blueprint('konsultasi', __name__)

@konsultasi_bp.route('/konsultasi', methods=['GET', 'POST'])
def konsultasi():
    if request.method == 'POST':
       
        form_data = request.form.to_dict() 
        
        analysis_results = get_expert_analysis(form_data)

        return render_template('hasil.html', results=analysis_results)
    
    return render_template('konsultasi.html')
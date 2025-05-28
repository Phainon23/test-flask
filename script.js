document.getElementById('predictionForm').addEventListener('submit', function(e) {
    e.preventDefault();
    

    const formData = {
        age: parseFloat(document.getElementById('age').value),
        sex: document.getElementById('sex').value,
        painful_Urination: parseFloat(document.getElementById('painful_Urination').value),
        vaginal_or_Penile_Discharge: document.getElementById('vaginal_or_Penile_Discharge').value,
        anal_itching: document.getElementById('anal_itching').value,
        sore_Throat: document.getElementById('sore_Throat').value,
    };
    
    const requestData = {
        inputs: [formData]
    };
    

    fetch('http://localhost:8000/api/hfp_prediction', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {

        const resultContainer = document.getElementById('resultContainer');
        resultContainer.style.display = 'block';
        
     
        const predictions = data.Prediction[0];
        let noAsthmaProb, asthmaProb;

        if (predictions.hasOwnProperty('0') && predictions.hasOwnProperty('1')) {
        
            noAsthmaProb = Math.round(predictions['0']);
            asthmaProb = Math.round(predictions['1']);
        } else {
            console.error('Unexpected API response format:', data);
            alert('Error processing prediction results');
            return;
        }
        
    
        document.getElementById('noAsthmaProb').textContent = noAsthmaProb + '%';
        document.getElementById('asthmaProb').textContent = asthmaProb + '%';
        
        
        document.getElementById('noAsthmaBar').style.width = noAsthmaProb + '%';
        
        document.getElementById('asthmaBar').style.width = asthmaProb + '%';
    })
});

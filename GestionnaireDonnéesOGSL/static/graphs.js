const context = document.getElementById('jeuMoissonee');
const context2 = document.getElementById('Rthematique');
const context3 = document.getElementById('Ttemporelle');

const thematiqueLabels = JSON.parse(context.dataset.labels)
const thematiqueValues = JSON.parse(context.dataset.values)
const _thematiqueValues = thematiqueValues.map(item=> item.total)

const myChart = new Chart(context, {
    type: 'bar',

    data: {
        labels: ['OpenGov','DonnéesQuébec','Boréalis','CanWin'],
        datasets: [{
            label: 'Nombre de jeux moissonnés par catalogue',
            data: _thematiqueValues,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)'

            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)'
            ],
            borderWidth: 1
        }]
    },
 
    options: {
        scales : {
            y: {
                beginAtZero: true
            }
        },
        
        layout : {
                padding : 20
            },
        responsive: true,
    }
});

const myChart2 = new Chart(context2, {
    type: 'doughnut',       
    data: {
        labels: thematiqueLabels,
        datasets: [{
            label: 'Répartition thématique des jeux de données',
            data: _thematiqueValues,
            backgroundColor: [
                'rgba(255, 99, 132, 0.5)',
                'rgba(54, 162, 235, 0.5)',
                'rgba(255, 206, 86, 0.5)',
                'rgba(75, 192, 192, 0.5)',
                'rgba(153, 102, 255, 0.5)',

                'rgba(5, 67, 100, 0.5)',
                'rgba(36, 4, 100, 0.5)',
                'rgba(4, 113, 24, 0.5)',
                'rgba(142, 163, 4, 0.5)',
                'rgba(83, 4, 240, 0.5)',
                'rgba(159, 56, 5, 0.5)',
                'rgba(125, 5, 5, 0.5)'

            ],
            borderColor: [
                'rgba(255, 255, 255, 1)',
                'rgba(255, 255, 255, 1)',
                'rgba(255, 255, 255, 1)',
                'rgba(255, 255, 255, 1)',
                'rgba(255, 255, 255, 1)',
                'rgba(255, 255, 255, 1)',
                'rgba(255, 255, 255, 1)',
                'rgba(255, 255, 255, 1)',
                'rgba(255, 255, 255, 1)',
                'rgba(255, 255, 255, 1)',
                'rgba(255, 255, 255, 1)',
                'rgba(255, 255, 255, 1)'
            ],
            borderWidth: 1,
            hoverOffset: 4,
            borderWidth: 3
        }]
    }
});


const labels = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'];
const myChart3 = new Chart(context3, {
    type: 'line',       
    data: {
        labels : labels,
        datasets: [{
            label: 'Nombre de requêtes par jour',
            data: [65, 59, 80, 81, 56, 55, 40],
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    }
});

        






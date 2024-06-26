export const barGraphOptions = {
    scales: {
        x: {
            title: {
                display: true,
                text: 'Period',
                font: {
                    size: 16,
                },
            },
            ticks: {
                font: {
                    size: 14, 
                },
            },
        },
        y: {
            title: {
                display: true,
                text: 'Amount',
                font: {
                    size: 16,
                },
            },
            ticks: {
                font: {
                    size: 14,
                },
            },
        },
    },
    plugins: {
        legend: {
            labels: {
                font: {
                    size: 16,
                },
            },
            position: 'top',
        },
        tooltip: {
            bodyFont: {
                size: 20,
            },
            titleFont: {
                size: 14,
            },
            padding: 12,

        },
    },
}

export const pieGraphOptions = {
        responsive: true,
    maintainAspectRatio: true,
    aspectRatio: 1.5,
    plugins: {
        legend: {
            labels: {
                font: {
                    size: 16,
                },
            },
            position: 'top',
        },
        tooltip: {
            bodyFont: {
                size: 18,
            },
            titleFont: {
                size: 20,
            },
            padding: 12,

        },
    },
    layout: {
        padding: {
            left: 150,
            right: 150,
            top: 50,
            bottom: 100,}
    }
};
export const updateBlog = [
    
    {
        date: '2024-05-07',
        title: 'Hello World!',
        description:    `This tool is still in its infancy. 
                        Some convenience features may be absent, and bugs might still arise. I'm striving to improve it. Nevertheless, i hope you can utilize the Costcatcher for your personal finance management.`,
        chapter: [
            {
                title: 'How To',
                icon: 'mdi-school',
                text: `Unfortunately, I have not created a proper tutorial yet. So just click around and see what happens.`,
                bullets: []
            },
            {
                title: 'Upcoming Features',
                icon: 'mdi-road-variant',
                text: `I already got some ideas for improvements. I do not know when I will implement them, but I will try to keep you updated.`,
                bullets: []
            },
        ]
    },
    {
        date: '2024-05-11',
        title: 'V1.1.0 | Never mind forgetting passwords',
        description:   ``,
        chapter: [
            {
                title: 'New Features / Changed',
                icon: 'mdi-party-popper',
                text: '',
                bullets: ['Password reset via email',
                            'minor design changes',
                        'created a 404-not-found page',
                            'improved the routing. Refreshes should now work properly',
                ]
            },
            {
                title: 'Bug Fixes',
                icon: 'mdi-bug',
                text: '',
                bullets: [  'crash when no data is uploaded while entering statistics or graphs',
                ]
            },
        ]
    },
    {
        date: '2024-05-07',
        title: 'V1.0.0 | The Beginning',
        description:   `Costcatcher is now online. 
                        I am excited to have created this platform and I am looking forward to the future. Enjoy and
                        feel free to reach out to me with any questions or feedback.`,
        chapter: [
            {
                title: 'New Features / Changed',
                icon: 'mdi-party-popper',
                text: '',
                bullets: [  'Import for csv-files implemented',
                            'Change your import schema in the settings menu',
                            'Category creation and management',
                            'Categorization of transactions via keyword matching',
                            'Basic table',
                            'Basic charts',
                ]
            },
        ]
    }
]
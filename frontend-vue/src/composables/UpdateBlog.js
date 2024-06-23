export const updateBlog = [
    {
        date: '2024-06-23',
        title: 'V2.1.0 | Seach and Filter',
        description:   `I added a more advanced search and filter functionality.`,
        chapter: [
            {
                title: 'New Features / Changed',
                icon: 'mdi-party-popper',
                text: '',
                bullets: ['New review page where you can see all your transactions',
                        'Filter categories in the statistics page',
                ]
            }
        ]
    }, 
       {
        date: '2024-05-26',
        title: 'V2.0.0 | A huge leap forward',
        description:   `Already in version 2.0? Yes, the backend has changed vastly and is not compatible with the previous version. Luckily, no one except me was using it.`,
        chapter: [
            {
                title: 'New Features / Changed',
                icon: 'mdi-party-popper',
                text: '',
                bullets: ['Huge performance improvements',
                        'Manual upload of single transactions is now possible',
                        'Statistics tableau with new filtering system',
                    'Graphs with new filtering system',
                        'Minor design tweaks',
                ]
            }
        ]
    }, 
    {
        date: '2024-05-11',
        title: 'V1.1.0 | Forget about worrying over your password',
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
export const Tutorials = [
  {
        id:"import",
        title: 'Import Data Tutorial',
        chapter: [
          {
            title: 'Download a csv file',
            text: 'Download a csv file from your bank or credit card provider. You will probably find this option in the transaction history section of your account.',
          },
          {
            title: 'Import the csv file',
            text: 'Use the file import field to select the donwloaded csv file. Costcatcher will try to display the content of the file in a table.'
          },
          {
            title: 'Change the import settings',
            text: 'You will most likely have to adjust the import settings to match the format of the csv file. This includes the date format, the column separator, and the column mapping. You can do this in the tab `CSV SETTINGS` in the settings menu.'
          },
          {
            title: 'Review the imported data',
            text: 'Check if the imported data looks correct. If not, try to change the `CSV SETTINGS` accordingly.'
          },
        ]
    },
      {
        id:"categorization",
        title: 'Categorization Tutorial',
        chapter: [
          {
            title: 'Basics',
            text: `Costcatcher supports an automatic categorization of your transactions based on custom rules.
              You will create rulesets that search for certain keywords in your transaction data and assign a category to the transaction if a keyword is found.
              You can see which transaction are not categorized yet in the <span class="text-button">TRANSACTION WITHOUT CATEGORIZATION</span> section. You can work your way through this section until everything is assigned.
              When you upload more data in the future, the ruleset will be applied to the new data as well.`,
          },
          {
            title: 'Create categories',
            text: 'Use <span class="text-button text-accent">EDIT CATEGORIES</span> to create new categories or edit existing ones. You can also assign a color to each category.'
          },
          {
            title: 'Create a ruleset',
            text: 'Use the fields in the <span class="text-button">RULESETS</span> section to create a ruleset, which searches for a specific keyword in your data and assigns a category to the transaction if the keyword is found.'
          },
          {
            title: 'Conflicts',
            text: 'An <span class="text-button">ICON</span> will appear if you created a ruleset has a conflict with another ruleset or when your rulseset is not leading to any categorization.'
          },
        ]
    },
]
  
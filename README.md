# CS50x Final Project
final project: localised finance tracker
components: 
*main user interface
*calculators (backend?)
*report window
*add entry window
*spending calculator window with sheet
*overview window
*search window(provides sum of provided entries)(filtered by date range and text)
*csv file
*read me/guide

categories:    necessary       | unnecessary        | groceries  | Restaurant | temporary    | taxable       | non-taxable
subcategories: business        |entertainment       | for home   | alone      | subscriptions| income/wage   | contribution	 
	       	   bills/utilities |gifts               | for others | with others|	             | interest      | gift
	       	   education       |shopping					             | capital gains | refund
	       	   medical         |super contributions |					     | shares        | termination payment
	           insurance       |
	           travel

expenses:
necessary: expenses related to non-consumable assets or services deemed required for the preservation of the person and assets used for necessary day to day activities 
unnecessary: expenses related to non-consumable assets or services not deemed required for the preservation of the person
groceries: expenses related to consumables deemed required for the preservation of the person or others
Restaurant: expenses related to consumables not deemed required for the preservation of a person or could have been alternatively sourced
temporary: foreseen unnecessary expenses or repeated payments that are not required for the preservation of a person

revenues:
taxable: revenue that is taxable by the relevant government
non-taxable: revenue that is non-taxable by the relevant government

csv headers:
code | entity | amount | category | sub-category | description | date


search bar: entity/description |category |sub-category | date range
search returns: number of transactions relating the search | the amount

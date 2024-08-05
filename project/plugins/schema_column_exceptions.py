class SchemaColumnExceptions:
    def __init__(self):
        self.exceptions = {}

    def add_exceptions(self, table_name, columns):
        """Add exceptions for a specific table."""
        self.exceptions[table_name] = columns

    def get_exceptions(self, table_name):
        """Get exceptions for a specific table."""
        return self.exceptions.get(table_name, [])

    def get_all_exceptions(self):
        """Get all exceptions across all tables."""
        return [col for exceptions in self.exceptions.values() for col in exceptions]

    def __str__(self):
        """String representation of all exceptions."""
        return str(self.exceptions)
    

# Create an instance and add exceptions
COLUMN_EXCEPTIONS = SchemaColumnExceptions()

COLUMN_EXCEPTIONS.add_exceptions('biblio', [
    'medium', 'part_number', 'part_name', 'unititle', 'notes', 'serial',
    'seriestile', 'copyrightdate', 'abstract'
])

COLUMN_EXCEPTIONS.add_exceptions('biblioitems', [
    'volume', 'number', 'issn', 'ean', 'publicationyear', 'publishercode',
    'volumedate', 'volumedesc', 'collectiontitle', 'collectionissn',
    'collectionvolume', 'editionstatement', 'editionresponsibility', 'notes',
    'size', 'place', 'lccn', 'url', 'cn_class', 'cn_item', 'cn_suffix',
    'cn_sort', 'agerestriction', 'totalissues'
])

COLUMN_EXCEPTIONS.add_exceptions('items', [
    'replacementprice', 'replacementpricedate', 'datelastborrowed', 'stack',
    'damaged', 'damaged_on', 'itemlost', 'itemlost_on', 'withdrawn',
    'withdrawn_on', 'coded_location_qualifier', 'issues', 'renewals',
    'reserves', 'restricted', 'itemnotes', 'itemnotes_nonpublic', 'deleted_on',
    'onloan', 'materials', 'uri', 'more_subfields_xml', 'enumchron',
    'new_status', 'exclude_from_local_holds_priority'
])
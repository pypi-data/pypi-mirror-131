use std::collections::HashMap;
use tantivy::collector::{Count, TopDocs};
use tantivy::directory::MmapDirectory;
use tantivy::schema::{IndexRecordOption, Schema, Term, STORED, STRING, TEXT};
use tantivy::{
    doc,
    query::{BooleanQuery, Query, QueryParser, TermQuery},
    Index,
};

pub fn update_index(
    index_path: &str,
    packages: Vec<HashMap<String, String>>,
) -> tantivy::Result<()> {
    let mut schema_builder = Schema::builder();
    let prefix = schema_builder.add_text_field("prefix", STRING | STORED);
    let cpn = schema_builder.add_text_field("cpn", STRING | STORED);
    let category = schema_builder.add_text_field("category", TEXT | STORED);
    let package_name = schema_builder.add_text_field("package", TEXT | STORED);
    let name = schema_builder.add_text_field("name", TEXT | STORED);
    let desc = schema_builder.add_text_field("desc", TEXT | STORED);
    let longdescription = schema_builder.add_text_field("longdescription", TEXT | STORED);
    let homepage = schema_builder.add_text_field("homepage", STRING | STORED);
    let other_homepages = schema_builder.add_text_field("other_homepages", STORED);
    let license = schema_builder.add_text_field("license", TEXT | STORED);
    let maintainer = schema_builder.add_text_field("maintainer", TEXT | STORED);
    let upstream_maintainer = schema_builder.add_text_field("upstream.maintainer", TEXT | STORED);
    let upstream_doc = schema_builder.add_text_field("upstream.doc", STRING | STORED);
    let upstream_bugs_to = schema_builder.add_text_field("upstream.bugs-to", STRING | STORED);
    let upstream_changelog = schema_builder.add_text_field("upstream.changelog", STRING | STORED);
    let schema = schema_builder.build();

    let index = Index::open_or_create(MmapDirectory::open(index_path)?, schema)?;
    let mut index_writer = index.writer(100_000_000)?;

    for package in packages {
        index_writer.add_document(doc!(
            prefix => package["prefix"].clone(),
            cpn => package["cpn"].clone(),
            category => package["category"].clone(),
            package_name => package["package"].clone(),
            name => package["name"].clone(),
            desc => package["desc"].clone(),
            longdescription => package.get("longdescription").unwrap_or(&String::new()).clone(),
            homepage => package.get("homepage").unwrap_or(&String::new()).clone(),
            other_homepages => package.get("other_homepages").unwrap_or(&String::new()).clone(),
            license => package.get("license").unwrap_or(&String::new()).clone(),
            maintainer => package.get("maintainer").unwrap_or(&String::new()).clone(),
            upstream_maintainer => package.get("upstream.maintainer").unwrap_or(&String::new()).clone(),
            upstream_doc => package.get("upstream.doc").unwrap_or(&String::new()).clone(),
            upstream_bugs_to => package.get("upstream.bugs-to").unwrap_or(&String::new()).clone(),
            upstream_changelog => package.get("upstream.changelog").unwrap_or(&String::new()).clone(),
        ));
    }

    index_writer.commit()?;
    Ok(())
}

/// Returns a json representation of the packages resulting from the query.
pub fn query(
    index_path: &str,
    prefix: &str,
    query: &str,
    limit: usize,
) -> tantivy::Result<Vec<String>> {
    let index = Index::open(MmapDirectory::open(index_path)?)?;
    let searcher = index.reader()?.searcher();
    let schema = index.schema();

    let query_parser = QueryParser::for_index(
        &index,
        vec![
            schema.get_field("category").unwrap(),
            schema.get_field("package").unwrap(),
            schema.get_field("name").unwrap(),
            schema.get_field("desc").unwrap(),
            schema.get_field("longdescription").unwrap(),
        ],
    );
    let prefix_term_query: Box<dyn Query> = Box::new(TermQuery::new(
        Term::from_field_text(schema.get_field("prefix").unwrap(), prefix),
        IndexRecordOption::Basic,
    ));
    let query = query_parser.parse_query(query)?;
    let query = BooleanQuery::intersection(vec![query, prefix_term_query]);
    let (top_docs, _) = searcher.search(&query, &(TopDocs::with_limit(limit), Count))?;

    let mut results = vec![];

    for (_, doc_address) in top_docs {
        results.push(schema.to_json(&searcher.doc(doc_address)?));
    }
    Ok(results)
}

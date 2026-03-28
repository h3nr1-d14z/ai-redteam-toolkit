Generate custom wordlist for: $ARGUMENTS

1. **Target intelligence**: Gather target-specific terms — company name, products, employee names, locations, years
2. **Base words**: Compile base word list from recon data, website scraping, social media
3. **Mutations**: Apply transformations — capitalization, leet speak, common substitutions (a->@, s->$, o->0)
4. **Patterns**: Generate common patterns — Word+Number, Word+Year, Word+Special, Season+Year, Company+Number
5. **Combinations**: Combine base words with common suffixes/prefixes (123, !, 2024, @company)
6. **Tool generation**: Use CeWL for website scraping, CUPP for personal wordlists, hashcat rules for mutation
7. **Deduplicate**: Remove duplicates, sort by likelihood, output in required format

Tools: CeWL, CUPP, hashcat --stdout with rules, custom Python scripts
Save to `wordlists/<target>-custom.txt`

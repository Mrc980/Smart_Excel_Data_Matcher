def export_results(matches, output_file):
    matches.to_excel(
        output_file,
        index=False
    )
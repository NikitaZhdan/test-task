from collections import defaultdict

from reports.base import BaseReport


class AverageGdpReport(BaseReport):
    def generate(self, data):
        gdp_by_country = defaultdict(list)

        for row in data:
            country = row.get("country")
            gdp_str = row.get("gdp")
            if country and gdp_str:
                try:
                    gdp = float(gdp_str)
                    gdp_by_country[country].append(gdp)
                except (ValueError, TypeError):
                    continue

        results = []
        for country, gdp_values in gdp_by_country.items():
            avg = sum(gdp_values) / len(gdp_values)
            results.append({
                "country": country,
                "gdp": round(avg, 2)
            })

        results.sort(key=lambda x: x["gdp"], reverse=True)
        return results

    def get_headers(self):
        return ["country", "gdp"]

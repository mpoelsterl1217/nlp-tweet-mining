from fuzzywuzzy import fuzz


class IMDB:

    people_by_nconst = {}
    originalTitle_by_tconst = {}
    primaryTitle_by_tconst = {}

    def __init__(self, awards_year):
        
        with open("imdb_data/name.basics.tsv") as file:
            next(file)
            for line in file:
                parts = line.split("\t")
                nconst = parts[0]
                primaryName = parts[1]
                birthYear = parts[2]
                deathYear = parts[3]

                ## Heuristic of if IMDB has no birth and death information, they are not important enough to win or be nominated
                #if deathYear == "\\N" and birthYear == "\\N":
                    #continue

                if deathYear == "\\N":
                    deathYear = None
                else:
                    deathYear = int(deathYear)

                if deathYear != None and deathYear < awards_year - 1:
                    continue
                else:
                    self.people_by_nconst[nconst] = primaryName

        with open("imdb_data/title.basics.tsv") as file:
            next(file)
            for line in file:
                parts = line.split("\t")
                tconst = parts[0]
                titleType = parts[1]
                primaryTitle = parts[2]
                originalTitle = parts[3]
                isAdult	= parts[4]
                startYear = parts[5]
                endYear	= parts[6]
                runtimeMinutes = parts[7]
                genres = parts[8]

                # Ignore TV series that ended before this awards year
                if titleType == "tvSeries" and endYear != "\\N" and int(endYear) < awards_year - 1:
                    continue

                # Ignore TV series that began after this awards year
                if titleType == "tvSeries" and startYear != "\\N" and int(startYear) > awards_year:
                    continue

                # For any other type of title, ignore it if it was released a before or after this year
                if titleType != "tvSeries" and startYear != "\\N" and (int(startYear) < awards_year - 1 or int(startYear) > awards_year):
                    continue

                self.primaryTitle_by_tconst[tconst] = primaryTitle
                self.originalTitle_by_tconst[tconst] = originalTitle
                


    def is_person_fuzzy(self, maybe_person: str) -> bool:
        threshold = 90
        found_person_fuzzy = False

        for person in self.people_by_nconst.values():
            '''
            if maybe_person in person:
                found_person_fuzzy = True
                print(f"{maybe_person} is a substring of {person}")
                break
            '''
            if fuzz.ratio(maybe_person, person) >= threshold:
                found_person_fuzzy = True
                print(f"{maybe_person} matches {person}, ratio: {fuzz.partial_ratio(maybe_person, person)}")
                break
        
        return found_person_fuzzy

    def is_title_fuzzy(self, maybe_title: str) -> bool:
        threshold = 90

        found_title_fuzzy = False

        for primaryTitle in self.primaryTitle_by_tconst.values():
            if fuzz.ratio(maybe_title, primaryTitle) >= threshold:
                found_title_fuzzy = True
                break

        if not found_title_fuzzy:
            for originalTitle in self.originalTitle_by_tconst.values():
                if fuzz.ratio(maybe_title, originalTitle) >= threshold:
                    found_title_fuzzy = True
                    break

        return found_title_fuzzy
        
        
if __name__ == "__main__":

    test_good_names = ["Angelina Jolie", "Angelina", "Jolie", "Chris"]
    test_bad_names = ["1960", "foobar", "calculate"]

    test_good_titles = ["Iron Man", "Gravity", "The Hobbit", "Oz"]
    test_bad_titles = ["Jennifer's Body", "Titane"]

    db = IMDB(2013)
    for name in test_good_names:
        print(f"{name}: {db.is_person_fuzzy(name)}")
    for name in test_bad_names:
        print(f"{name}: {db.is_person_fuzzy(name)}")

    for title in test_good_titles:
        print(f"{title}: {db.is_title_fuzzy(title)}")
    for title in test_bad_titles:
        print(f"{title}: {db.is_title_fuzzy(title)}")
    

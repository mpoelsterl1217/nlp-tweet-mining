from fuzzywuzzy import fuzz

class IMDB:

    people_by_nconst = {}
    originalTitle_by_tconst = {}
    primaryTitle_by_tconst = {}
    writers_by_tconst = {}
    directors_by_tconst = {}

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

        with open("imdb_data/title.crew.tsv") as file:
            next(file)

            for line in file:
                parts = line.split("\t")
                tconst = parts[0]
                directors = parts[1].split(",")
                writers = parts[2].split(",")

                # We can ignore this title if the tconst is not in our other dictionaries
                if self.originalTitle_by_tconst.get(tconst) == None and self.primaryTitle_by_tconst.get(tconst) == None:
                    continue

                self.directors_by_tconst[tconst] = directors
                self.writers_by_tconst[tconst] = writers

                
    def is_person_fuzzy(self, maybe_person: str) -> bool:
        return self._find_person_fuzzy(maybe_person) != []

    def is_title_fuzzy(self, maybe_title: str) -> bool:
        return self._find_title_fuzzy(maybe_title) != []

    def _find_person_fuzzy(self, maybe_person: str):
        nconsts = []
        for nconst in self.people_by_nconst.keys():
            person = self.people_by_nconst[nconst]
            if self._fuzzy_person_match(maybe_person, person):
                print(f"{maybe_person} matches {person} ({nconst})")
                nconsts.append(nconst)
        
        return nconsts

    def _find_title_fuzzy(self, maybe_title: str):
        tconsts = []
        for tconst in self.primaryTitle_by_tconst.keys():
            title = self.primaryTitle_by_tconst[tconst]
            if self._fuzzy_title_match(maybe_title, title):
                print(f"{maybe_title} matches {title}({tconst})")
                tconsts.append(tconst)

        for tconst in self.originalTitle_by_tconst.keys():
            title = self.originalTitle_by_tconst[tconst]
            if self._fuzzy_title_match(maybe_title, title):
                print(f"{maybe_title} matches {title} ({tconst})")
                tconsts.append(tconst)
        
        return tconsts


    def _fuzzy_people_match(self, p1, p2):
        threshold = 90
        return fuzz.ratio(p1, p2) >= threshold or p1 in p2
    
    def _fuzzy_title_match(self, t1, t2):
        threshold = 90
        return fuzz.ratio(t1, t2) >= threshold or t1 in t2


    def title_is_directed_by(self, title, maybe_director):
        tconsts = self._find_title_fuzzy(title)
        if tconsts == []:
            return False

        for tconst in tconsts:
            directors = []
            if self.directors_by_tconst.get(tconst) != None:
                directors = [self.people_by_nconst[nconst] for nconst in self.directors_by_tconst[tconst] if self.people_by_nconst.get(nconst) != None]
            print(f"Title {tconst} is directed by {directors}")
            for director in directors:
                if self._fuzzy_people_match(maybe_director, director):
                    return True
                print(f"{maybe_director} and {director} do not match")
            
        return False

    def title_is_written_by(self, title, maybe_writer):
        tconsts = self._find_title_fuzzy(title)
        if tconsts == []:
            return False

        for tconst in tconsts:
            writers = []
            if self.writers_by_tconst.get(tconst) != None:
                writers = [self.people_by_nconst[nconst] for nconst in self.writers_by_tconst[tconst] if self.people_by_nconst.get(nconst) != None]
            for writer in writers:
                if self._fuzzy_people_match(maybe_writer, writer):
                    return True

        return False

    
        
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
    

#include <algorithm> 
#include <iostream>
#include <map>
#include <string>
#include <vector>
#include <memory>

using namespace std;

// Command: g++ -std=c++11 analysis.cpp -o main && ./main

struct State {
    string name;
    long score;

    State(const string& name, long score) : name(name), score(score) {};
};

const State CA("california", 39538223);
const State TX("texas", 29145505);
const State FL("florida", 21538187);
const State NY("newyork", 20201249);
const State PA("pennsylvania", 13002700);
const State IL("illinois", 12812508);
const State OH("ohio", 11799448);
const State GA("georgia", 10711908);
const State NC("northcarolina", 10439388);
const State MI("michigan", 10077331);
const State NJ("newjersey", 9288994);
const State VI("virginia", 8631393);
const State WA("washington", 7705281);
const State AZ("arizona", 7151502);
const State MA("massachusetts", 7029917);
const State TN("tennessee", 6910840);
const State IN("indiana", 6785528);
const State MD("maryland", 6177224);
const State MO("missouri", 6154913);
const State WI("wisconsin", 5893718);
const State CO("colorado", 5773714);
const State MN("minnesota", 5706494);
const State SC("southcarolina", 5118425);
const State AL("alabama", 5024279);
const State LA("louisiana", 4657757);
const State KY("kentucky", 4505836);
const State OR("oregon", 4237256);
const State OK("oklahoma", 3959353);
const State CT("connecticut", 3605944);
const State UT("utah", 3271616);
const State IA("iowa", 3190369);
const State NV("nevada", 3104614);
const State AR("arkansas", 3011524);
const State MS("mississippi", 2961279);
const State KS("kansas", 2937880);
const State NM("newmexico", 2117522);
const State NE("nebraska", 1961504);
const State ID("idaho", 1839106);
const State WV("westvirginia", 1793716);
const State HI("hawaii", 1455271);
const State NH("newhampshire", 1377529);
const State ME("maine", 1362359);
const State RI("rhodeisland", 1097379);
const State MT("montana", 1084225);
const State DE("delaware", 989948);
const State SD("southdakota", 886667);
const State ND("northdakota", 779094);
const State VT("vermont", 643077);
const State WY("wyoming", 576851);

State STATES[49] = {CA, TX, FL, NY, PA, IL, OH, GA, NC, MI,
                    NJ, VI, WA, AZ, MA, TN, IN, MD, MO, WI,
                    CO, MN, SC, AL, LA, KY, OR, OK, CT, UT,
                    IA, NV, AR, MS, KS, NM, NE, ID, WV, HI,
                    NH, ME, RI, MT, DE, SD, ND, VT, WY};

template <typename T, typename U>
bool sortDescending(pair<T, U>& a, pair<T, U>& b) {
    return a.second > b.second;
}

template <typename T, typename U>
vector<pair<T, U>> buildDescendingList(unordered_map<T, U> map) {
    vector<pair<T, U>> list;
    for (auto& pair : map) {
        list.emplace_back(pair);
    }
    sort(list.begin(), list.end(), sortDescending<T, U>);
    return list;
}

template <typename U, typename V>
vector<U> getKeys(unordered_map<U, V> map) {
    vector<U> keys;
    for (const auto& [key, value] : map) {
        keys.emplace_back(key);
    }
    return keys;
}

int main() {
    // for (auto& state : STATES) {
    //     auto& name = state.name;

    //     float lowestValue;
    //     char lowestValueChar = '\0';
    //     for (int i = 0; i < name.size(); ++i) {
    //         float value = scorePerLetter[name.at(i)];

    //         if (lowestValueChar == '\0' || value < lowestValue) {
    //             lowestValue = value;
    //             lowestValueChar = name.at(i);
    //         }
    //     }
    //     cout << "Lowest value letter for '" << name << "': " << lowestValueChar << endl;
    // }

    unordered_map<char, unordered_map<char, float>> neighbourLetterScore;
    for (auto& state : STATES) {
        auto& name = state.name;
        auto length = name.size();

        for (int i = 0; i < length; ++i) {
            if (i < length-1) {
                neighbourLetterScore[name.at(i)][name.at(i+1)] += float(state.score) / length;
            }
            if (i > 0) {
                neighbourLetterScore[name.at(i)][name.at(i-1)] += float(state.score) / length;
            }
        }
    }

    // Normalize the scores
    for (auto& [letter, neighbourMap] : neighbourLetterScore) {
        long totalScore = 0;
        for (const auto& [neighbour, neighbourScore] : neighbourMap) {
            totalScore += neighbourScore;
        }
        for (const auto& [neighbour, neighbourScore] : neighbourMap) {
            neighbourMap[neighbour] /= totalScore;
        }
    }

    unordered_map<char, float> scorePerLetter;
    for (auto& state : STATES) {
        auto& name = state.name;
        size_t length = name.size();
        for (int i = 0; i < length; ++i) {
            scorePerLetter[name.at(i)] += float(state.score) / length;
        }
    }
    vector<char> letters = getKeys<char, float>(scorePerLetter);

    // Print out letters in order of score
    sort(letters.begin(), letters.end(), [&](char first, char second) {
        return scorePerLetter[first] > scorePerLetter[second];
    });
    for (auto& letter : letters) {
        unordered_map<char, float>& scores = neighbourLetterScore[letter];
        vector<char> neighbours = getKeys<char, float>(scores);
        sort(neighbours.begin(), neighbours.end(), [&](char first, char second) {
            return scores[first] > scores[second];
        });

        cout << "---- NEIGHBOUR SCORES for " << letter << " -----" << endl;
        for (auto& neighbour : neighbours) {
            cout << "Score for " << neighbour << ": " << scores[neighbour] << endl;
        }
        cout << endl;
    }
}

void calculateNGrams(vector<string>& stateNames) {
    const int MAX_NGRAMS = 5;

    for (int N = 1; N <= MAX_NGRAMS; ++N) {
        cout << "---- CALCULATING N-GRAMS for N= " << N << " ----" << endl;

        unordered_map<string, long> nGrams;
        for (auto& name : stateNames) {
            for (int i = 0; i < name.size()-(N-1); ++i) {
                string nGram = name.substr(i, N);
                sort(nGram.begin(), nGram.end());
                nGrams[nGram]++;
            }
        }
        auto nGramsInOrder = buildDescendingList<string, long>(nGrams);
        for (int i = 0; i < 5; ++i) {
            auto& pair = nGramsInOrder.at(i);
            cout << "N-gram: " << pair.first << ", Score: " << pair.second << endl;
        }
        cout << endl;
    }
}

void calculateDistances(vector<string>& stateNames) {
    const int MAX_DIST = 4;

    for (int K = 2; K <= MAX_DIST; ++K) {
        cout << "---- CALCULATING K-DIST for K= " << K << " ----" << endl;

        unordered_map<string, long> distanceOfK;
        for (auto& name : stateNames) {
            for (int i = 0; i < name.size()-K; ++i) {
                char pair[2] = {name.at(i), name.at(i+K)};
                distanceOfK[string(pair)] += 1;
            }
        }
        auto kDistLettersInOrder = buildDescendingList<string, long>(distanceOfK);
        for (int i = 0; i < 5; ++i) {
            auto& pair = kDistLettersInOrder.at(i);
            cout << "K-dist pair: " << pair.first << ", Score: " << pair.second << endl;
        }
        cout << endl;
    }
}

long score(char grid[5][5]) {
    return 0;
}

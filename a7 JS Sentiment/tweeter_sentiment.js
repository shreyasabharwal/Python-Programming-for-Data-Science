'use strict';


// 1. A function to split up the tweet's text (a string) into individual words (an array)
function splitIntoWords(tweet) {
    var lstWords = tweet.split(/\W+/);
    // convert all words to lowercase
    var lstWords = lstWords.map(function (item) {
        return item.toLowerCase();
    });
    // return all words having length greater than 1
    var wordList = lstWords.filter(function (item) {
        return (item.length > 1);
    });
    return wordList;
}


// 2. A function that filters an array of words to only get those words that contain a specific emotion
function filterWordsForEmotion(wordList, emotion) {
    var filteredList = wordList.filter(function (word) {
        if (word in SENTIMENTS && emotion in SENTIMENTS[word]) {
            return word;
        }
    });
    return filteredList;
}


// 3. A function that determines which words from an array have each emotion, returning an object that contains that information
function categorizeByEmotions(wordList) {
    var wordsCategorizedByEmotion = EMOTIONS.reduce(function (filteredWords, emotion) {
        if (!filteredWords[emotion]) {
            filteredWords[emotion] = [];
        }
        filteredWords[emotion].push(filterWordsForEmotion(wordList, emotion));
        return filteredWords;
    }, {});
    return wordsCategorizedByEmotion;
}


// 4. A function that gets an array of the "most common" words in an array, ordered by their frequency
function sortWordsByFrequency(wordList) {
    //store word counts and words as key-value pairs
    var objWordCount = wordList.reduce(function (wordCount, word) {
        if (!wordCount[word]) {
            wordCount[word] = 0;
        }
        wordCount[word] = wordCount[word] + 1;
        return wordCount;
    }, {});

    var items = Object.keys(objWordCount).map(function (key) {
        return [key, objWordCount[key]];
    });
    // sort array by values of keys in descending order
    items.sort(function (first, second) {
        return (second[1] - first[1]);
    });

    //push keys in descending order of their counts
    var listItems = [];
    items.forEach(function (item) {
        listItems.push(item[0]);
    });
    return listItems;
}


// 5. Function to return an array of all words included in those tweets 
function getAllWords(arrTweets) {
    var lstTweets = arrTweets.reduce(function (listTweets, tweet) {
        listTweets = listTweets.concat(splitIntoWords(tweet['text']))
        return listTweets;
    }, []);
    return lstTweets;
}


// 6. Function to return an array of hashtags used in tweets
function getEmotionHashtags(arrTweets, emotion) {
    // getting tweets having at least one word with that emotion
    var filteredTweets = arrTweets.filter(function (tweet) {
        var wordList = splitIntoWords(tweet['text']);
        var emotionObj = filterWordsForEmotion(wordList, emotion)
        if (emotionObj.length > 0) {
            return tweet;
        }
    });

    // extracting hashtags of the filtered tweets
    var listHashtags = filteredTweets.reduce(function (hashtags, tweet) {
        for (var i = 0; i < tweet['entities']['hashtags'].length; i++) {
            hashtags = hashtags.concat('#' + tweet['entities']['hashtags'][i]['text'].toLowerCase());
        }
        return hashtags;
    }, []);
    return listHashtags;
}


// 7. Function to create a data structure to store all the tweets data to be displayed on screen
function analyzeTweets(arrTweets) {
    var wordList = getAllWords(arrTweets);
    var numOfWords = wordList.length;
    // store required data to be displayed in an object
    var dtEmotions = EMOTIONS.reduce(function (objEmotions, emotion) {
        objEmotions[emotion] = [];
        objEmotions[emotion]['Hashtags'] = [];
        objEmotions[emotion]['Example Words'] = [];
        objEmotions[emotion]['Hashtags'] = getEmotionHashtags(arrTweets, emotion);
        objEmotions[emotion]['Example Words'] = filterWordsForEmotion(wordList, emotion);
        objEmotions[emotion]['%age Words'] = parseFloat(((objEmotions[emotion]['Example Words'].length / numOfWords) * 100).toFixed(2));
        return objEmotions;
    }, {});

    // sort hashtags and example words in descending order of frequency of occurence
    var dsEmotions = EMOTIONS.reduce(function (objEmotions, emotion) {
        objEmotions[emotion]['Hashtags'] = sortWordsByFrequency(objEmotions[emotion]['Hashtags']);
        objEmotions[emotion]['Example Words'] = sortWordsByFrequency(objEmotions[emotion]['Example Words']);
        return objEmotions;
    }, dtEmotions);

    return dsEmotions;
}


// Display Statistics of the data pulled from Twitter
function showEmotionData(objOfEmotions) {
    var element = d3.select('#emotionsTableContent')
    element.html('');
    // Sorting object by %age Words
    var obj = Object.keys(objOfEmotions).sort(function (a, b) {
        return objOfEmotions[b]['%age Words'] - objOfEmotions[a]['%age Words']
    });

    // display information as table
    obj.forEach(function (emotion) {
        var str1 = emotion;
        var str2 = objOfEmotions[emotion]['%age Words'] + '%';
        var str3 = objOfEmotions[emotion]['Example Words'].slice(0, 3).join(", ").toLowerCase();
        var str4 = objOfEmotions[emotion]['Hashtags'].slice(0, 3).join(", ").toLowerCase();
        var strLtrl = `<td>${str1}</td><td>${str2}</td><td>${str3}</td><td>${str4}</td>`
        element.append('tr').html(strLtrl);
    });
}

// Function to get Live Data from Twitter for a particular username
async function loadTweets(userName) {
    var searchuri = '  https://faculty.washington.edu/joelross/proxy/twitter/timeline/?' + 'screen_name=' + userName;
    var tweetsData = await d3.json(searchuri);
    showEmotionData(analyzeTweets(tweetsData));
}


// fetching Twitter username entered by user and extracting tweets for that username
showEmotionData(analyzeTweets(SAMPLE_TWEETS));
var button1 = d3.select('#searchButton');
button1.on('click', function () {
    var val = d3.select('#searchBox').property('value');
    loadTweets(val);
});
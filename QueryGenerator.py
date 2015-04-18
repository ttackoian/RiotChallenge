import scipy.io
import sys

champion2Feature = {
	"Jax" : 1,
	"Twisted Fate" : 67,
	"Kennen" : 56,
	"Shaco" : 2,
	"Warwick" : 3,
	"Nidalee" : 4,
	"Zyra" : 5,
	"Brand" : 6,
	"Rammus" : 7,
	"Corki" : 8,
	"Braum" : 9,
	"Sejuani" : 26,
	"Tryndamere" : 11,
	"Kha Zix" : 46,
	"Yorick" : 14,
	"Xerath" : 15,
	"Sivir" : 16,
	"Riven" : 17,
	"Orianna" : 18,
	"Gangplank" : 19,
	"Malphite" : 20,
	"Miss Fortune" : 12,
	"LeBlanc" : 122,
	"Poppy" : 21,
	"Lee Sin" : 102,
	"Karthus" : 22,
	"Jayce" : 23,
	"Nunu" : 24,
	"Trundle" : 25,
	"Graves" : 27,
	"Lucian" : 70,
	"Gnar" : 29,
	"Lux" : 30,
	"Shyvana" : 31,
	"Renekton" : 32,
	"Darius" : 73,
	"Fiora" : 33,
	"Jinx" : 34,
	"Kalista" : 35,
	"Fizz" : 36,
	"Kassadin" : 37,
	"Sona" : 38,
	"Vladimir" : 108,
	"Viktor" : 40,
	"Cassiopeia" : 41,
	"Maokai" : 42,
	"Thresh" : 43,
	"Kayle" : 44,
	"Hecarim" : 45,
	"Vel'Koz" : 85,
	"Olaf" : 47,
	"Ziggs" : 48,
	"Syndra" : 49,
	"Karma" : 51,
	"Annie" : 52,
	"Akali" : 53,
	"Volibear" : 71,
	"Yasuo" : 55,
	"Teemo" : 79,
	"Rengar" : 57,
	"Ryze" : 58,
	"Shen" : 59,
	"Zac" : 60,
	"Dr Mundo" : 50,
	"Pantheon" : 61,
	"Swain" : 62,
	"Bard" : 63,
	"Sion" : 64,
	"Vayne" : 65,
	"Nasus" : 66,
	"Fiddlesticks" : 99,
	"Udyr" : 69,
	"Rek Sai" : 107,
	"Morgana" : 28,
	"Leona" : 54,
	"Caitlyn" : 72,
	"Anivia" : 10,
	"Nocturne" : 74,
	"Zilean" : 75,
	"Azir" : 76,
	"Rumble" : 77,
	"Skarner" : 78,
	"Cho Gath" : 68,
	"Urgot" : 80,
	"Wukong" : 0,
	"Amumu" : 81,
	"Galio" : 82,
	"Heimerdinger" : 83,
	"Ashe" : 84,
	"Singed" : 86,
	"Varus" : 87,
	"Twitch" : 88,
	"Kog Maw" : 96,
	"Garen" : 89,
	"Blitzcrank" : 13,
	"Elise" : 92,
	"Alistar" : 93,
	"Katarina" : 94,
	"Mordekaiser" : 95,
	"Jarvan IV" : 109,
	"Aatrox" : 97,
	"Draven" : 98,
	"Talon" : 100,
	"Xin Zhao" : 101,
	"Ahri" : 120,
	"Malzahar" : 104,
	"Lissandra" : 105,
	"Diana" : 90,
	"Tristana" : 106,
	"Irelia" : 39,
	"Nami" : 110,
	"Soraka" : 111,
	"Veigar" : 112,
	"Janna" : 113,
	"Nautilus" : 114,
	"Evelynn" : 115,
	"Gragas" : 116,
	"Zed" : 117,
	"Vi" : 118,
	"Lulu" : 119,
	"Master Yi" : 91,
	"Taric" : 103,
	"Quinn" : 121,
	"Ezreal" : 123
}

numKeys = len(champion2Feature.keys())

def generateVector(featureNums):
	zeros = []
	for _ in range(numKeys):
		zeros.append(0)

	for index in featureNums:
		zeros[index] = 1

	return zeros

def main():

	queries = []

	while True:
		featureNums = []
		while len(featureNums) < 5:
			champ = raw_input("Enter name of champion : ")
			if champ in champion2Feature.keys():
				featureNums.append(champion2Feature[champ])
			else:
				print "That is not a valid champion"

		data_point = generateVector(featureNums)
		queries.append(data_point)
		next = raw_input("Make another query? (Yes/No)")
		if next == "Yes" or next == "yes" or next == "y":
			continue
		else:
			break

	fileDict = {"testData" : queries}
	scipy.io.savemat('testData.mat', fileDict)


if __name__ == "__main__":
	main()

# -*- coding: utf-8 -*-
import argparse
import plistlib
import numpy as np
from matplotlib import pyplot


def findCommonTracks(fileNames):
    trackNameSets = []
    for fileName in fileNames:
        trackNames = set()
        plist = plistlib.readPlist(fileName)
        tracks = plist['Tracks']
        for trackId, track in tracks.items():
            try:
                trackNames.add(track['name'])
            except:
                pass
    trackNameSets.append(trackNames)
    # set.intersection （交集）  *trackNameSets(展开参数列表)
    commonTracks = set.intersection(*trackNameSets)
    if len(commonTracks) > 0:
        f = open("common.txt", "wb")
        for val in commonTracks:
            s = "%s\n" % val
            f.write(s.encode("UTF-8"))
            f.close()
            print("%d common  tracks found."
                  "Track names written to common.txt" % len(commonTracks))
    else:
        print("No common tracks!")


def plotStats(fileName):
    plist = plistlib.readPlist(fileName)
    tracks = plist['Tracks']
    ratings = []
    durations = []
    for trackId, track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
        except:
            pass
    if ratings == [] or durations == []:
        print ("No valid Album Rating/Total Time data in %s." % fileName)
        return

    x = np.array(durations, np.int32)
    x = x / 60000.0
    y = np.array(ratings,np.int32)
    # 设置图应该有(两行/一列/下一个点在第一行)
    pyplot.subplot(2, 1, 1)
    # 用o来表示数据
    pyplot.plot(x, y, 'o')
    # 设置x,y 略大一点的范围,在图和轴之间留一些空间
    pyplot.axis([0, 1.05 * np.max(x), -1, 110])
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Track rating')

    pyplot.subplot(2, 1, 2)
    # 设置数据分区的个数
    pyplot.hist(x, bins=20)
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Count')

    pyplot.show()


def findDuplicates(fileName):
    print('Finding duplicate tracks in %s ...' % fileName)
    plist = plistlib.readPlist(fileName)
    tracks = plist['Tracks']
    trackNames = {}
    for trackId, track in tracks.items():
        try:
            name = track['name']
            duration = track['Total Time']
            if name in trackNames:
                if duration // 1000 == trackNames[name][0] // 1000:
                    count = trackNames[name][1]
                    trackNames[name] = (duration, count + 1)
                else:
                    trackNames[name] = (duration, 1)
        except:
            pass

    dups = []
    for k, v in trackNames.items():
        if v[1] > 1:
            dups.append((v[1], k))

        if len(dups) > 0:
            print('Found %d duplicates. Track names saved to dup.txt' % len(dups))
        else:
            print('No duplicate tracks found!')
        f = open("dups.txt", "wb")
        for val in dups:
            f.write("[%d] %s\n" % (val[0], val[1]))
        f.close()


def main():
    descStr = """
        This program analyzes playlist files (.xml) exported from iTunes.
    """
    parser = argparse.ArgumentParser(description=descStr)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--common', nargs='*', dest='plFiles', required=False)
    group.add_argument('--stats', dest='plFile', required=False)
    group.add_argument('--dup', dest='plFileD', required=False)

    args = parser.parse_args()
    if args.plFiles:
        findCommonTracks(args.plFiles)

    elif args.plFile:
        plotStats(args.plFile)

    elif args.plFilesD:
        findCommonTracks(args.plFilesD)

    else:
        print ("These are not the tracks you are looking for.")


if __name__ == '__main__':
    main()

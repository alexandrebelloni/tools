#!/usr/bin/pypy

import subprocess, re, sys, string
import logparser
import pickle
from patterns import patterns

FE = {}
versions=[]

map_authors = {
        'albin.tonnerre@free-electrons.com': 'Albin Tonnerre',
        'alexandre.belloni@bootlin.com': 'Alexandre Belloni',
        'alexandre.belloni@free-electrons.com': 'Alexandre Belloni',
        'antoine.tenart@bootlin.com': 'Antoine Tenart',
        'antoine.tenart@free-electrons.com': 'Antoine Tenart',
        'boris.brezillon@bootlin.com': 'Boris Brezillon',
        'boris.brezillon@free-electrons.com': 'Boris Brezillon',
        'cyrille.pitchen@free-electrons.com': 'Cyrille Pitchen',
        'david.wagner@free-electrons.com': 'David Wagner',
        'ezequiel.garcia@free-electrons.com': 'Ezequiel Garcia',
        'gregory.clement@bootlin.com': 'Gregory Clement',
        'gregory.clement@free-electrons.com': 'Gregory Clement',
        'maxime.chevallier@bootlin.com': 'Maxime Chevallier',
        'maxime.ripard@bootlin.com': 'Maxime Ripard',
        'maxime.ripard@free-electrons.com': 'Maxime Ripard',
        'michael@free-electrons.com': 'Michael Opdenacker',
        'michael-lists@free-electrons.com': 'Michael Opdenacker',
        'michael.opdenacker@bootlin.com': 'Michael Opdenacker',
        'michael.opdenacker@free-electrons.com': 'Michael Opdenacker',
        'miquel.raynal@bootlin.com': 'Miquel Raynal',
        'miquel.raynal@free-electrons.com': 'Miquel Raynal',
        'mylene.josserand@bootlin.com': 'Mylene Josserand',
        'mylene.josserand@free-electrons.com': 'Mylene Josserand',
        'paul.kocialkowski@bootlin.com': 'Paul Kocialkowski',
        'quentin.schulz@bootlin.com': 'Quentin Schulz',
        'quentin.schulz@free-electrons.com': 'Quentin Schulz',
        'romain.perier@free-electrons.com': 'Romain Perier',
        'thomas.petazzoni@bootlin.com': 'Thomas Petazzoni',
        'thomas.petazzoni@free-electrons.com': 'Thomas Petazzoni',
}

def makever(v):
    s=v.split('.')
    return 1000*int(s[0][1:])+int(s[1])

def add_commit(author, ver, sob):
    if ver == 'v2.6.39':
        ver = 'v2.6.x'
    if author in map_authors:
        author = map_authors[author]
    if author not in FE:
        FE[author] = {}
    if ver not in FE[author]:
        FE[author][ver] = [0, 0]
    FE[author][ver][sob] += 1


vcmd=["git", "tag", "-l", 'v[3-9].[0-9]', "-l", 'v[3-9].[0-9][0-9]']
#vcmd=["git", "tag", "-l", 'v[4-9].[0-9]']
v = subprocess.Popen(vcmd, stdout=subprocess.PIPE)
for line in v.stdout:
  if line != '':
    versions.append(line.rstrip())
  else:
    break

#for i in range(18,39):
#    versions.append("v2.6.%d" % (i))

versions.append("v2.6.11")
versions.append("v2.6.39")
v=sorted(versions, key=makever)
v.append('HEAD')

#logcmd=["git", "log", "--numstat", "-M", "%s..%s"]
logcmd=["git", "log", "%s..%s"]
prev=v[0]
for cur in v[1:]:
    print cur
    version = "%s..%s" % (prev, cur)
    logcmd = logcmd[:-1]
    logcmd.append(version)
    log = subprocess.Popen(logcmd, stdout=subprocess.PIPE).stdout

    patches = logparser.LogPatchSplitter(log)
    for patch in patches:
        m = patterns['commit'].match(patch[0])
        if not m:
            continue
        author=None
        sob=None
        merge=False
        for Line in patch[1:]:
            m = patterns['merge'].match(Line)
            if m:
                merge=True
                break
            m = patterns['author'].match(Line)
            if m:
                author = m.group(2)
                continue

            m = patterns['signed-off-by'].match(Line)
            if m:
                sob = m.group(2)
                continue

        if merge:
            continue

        if author and (("free-electrons.com" in author) or ("bootlin.com" in author)) and not author in map_authors:
            print "missing " + author

        if author and author in map_authors:
            add_commit(author, cur, 0)

        if sob and sob != author and sob in map_authors:
            add_commit(sob, cur, 1)

    prev = cur

v[1] = 'v2.6.x'
with open('gitdm.dump', 'w') as f:
    pickle.dump((v[1:], FE), f, pickle.HIGHEST_PROTOCOL)

from faker import Faker
from random import uniform, randint, shuffle
#import yaml
from tqdm import tqdm
from copy import deepcopy

fake = Faker()

###CONSTANT BLOCK
ROUND_THRESHOLD = 0.7

MAX_BLOC_SIZE = 0.5
MIN_BLOC_SIZE = 0.1
SUPERBLOC_SIZE = 0.7
MINIBLOC_SIZE = 0.075
STRAIGHT_BLOC_PCT = 0.65
BULLET_PCT = 0.25
###END CONSTANTS

config = {}
n_candidates = randint(3,15)
n_winners = randint(1,n_candidates-1)
n_blocs = randint(3,round(n_candidates*1.25))
n_ballots = randint(n_candidates*2, n_candidates*1000)
print('nc',n_candidates)
print('nw', n_winners)
print('nb',n_blocs)
print('nv', n_ballots)

def gen_blocs(n_blocs, n_candidates):
    print('Generating voting blocs...')
    blocs = []
    while len(blocs) < n_blocs:
        n_entries = randint(2,5 if n_candidates > 4 else n_candidates)
        thisbloc = []
        for _ in range(n_entries):
            cand = randint(0,n_candidates-1)
            while cand in thisbloc:
                cand = randint(0,n_candidates-1)
            thisbloc.append(cand)
        commit = True
        for b in blocs:
            if thisbloc[0] == b[0] and thisbloc[1] == b[1]:
                commit = False
        if commit and thisbloc not in blocs:
            blocs.append(deepcopy(thisbloc))
    return blocs

def decide_voters(blocs, n_candidates, n_ballots):
    print('Generating ballots...')
    ballots = []
    remaining = n_ballots
    allocations = [0] * (len(blocs) + 1)
    for i in tqdm(range(len(allocations))):
        hi_pct = MAX_BLOC_SIZE
        lo_pct = MIN_BLOC_SIZE
        if i < 3:
            if uniform(0,1) < 0.1:
                hi_pct = SUPERBLOC_SIZE
        else:
            if uniform(0,1) < 0.05:
                lo_pct = MINIBLOC_SIZE
        cand_allocs = round(remaining * uniform(lo_pct,hi_pct))
        if (remaining - cand_allocs) > 0:
            allocations[i] = cand_allocs
        else:
            allocations[i] = remaining
        remaining -= allocations[i]
        if remaining < 1:
            break
    allocations[-1] += remaining
    remaining = 0
    # allocate bloc ballots
    for i,bloc in enumerate(blocs):
        if allocations[i] < 1:
            continue
        straight_ballots = round(allocations[i] * STRAIGHT_BLOC_PCT *
                                 uniform(.9, 1.1))
        bullet_ballots = round(allocations[i] * BULLET_PCT * uniform(.9, 1.1))
        if len(bloc) < 3:
            while allocations[i] > straight_ballots + bullet_ballots:
                if uniform(0,1) > .2:
                    straight_ballots += 1
                else:
                    bullet_ballots += 1
        mod_ballots = 0
        if allocations[i] > straight_ballots + bullet_ballots:
            mod_ballots = allocations[i] - (straight_ballots + bullet_ballots)
        ballots.extend([deepcopy(bloc)] * straight_ballots)
        ballots.extend([[bloc[0]]] * bullet_ballots)
        if mod_ballots:
            possible_mods = []
            this_ballot = deepcopy(bloc)
            tail = this_ballot[1:]
            for j in range(len(tail)):
                possible_mods.append([tail[j]])
                cand = [[t for jj,t in enumerate(tail) if jj > j]]
                cand.append([t for jj,t in enumerate(tail) if j > jj])
                cand.append(cand[0] + [tail[j]])
                cand.append(cand[1] + [tail[j]])
                for c in cand:
                    if c not in possible_mods:
                        possible_mods.append(c)
            shuffle(possible_mods)
            for pm in possible_mods[:-1]:
                if not mod_ballots:
                    break
                if mod_ballots == 1:
                    mod_ballots = 0
                    ballots.append(pm)
                else:
                    drop = round(mod_ballots * uniform(0.4,1))
                    if drop:
                        mod_ballots -= drop
                        ballots.extend([deepcopy(pm)] * drop)
            ballots.extend([deepcopy(possible_mods[-1])] * mod_ballots)

    #allocate non-bloc ballots
    for _ in tqdm(range(allocations[-1])):
        places = randint(1,n_candidates)
        voted = []
        for _ in range(places):
            selection = randint(0,n_candidates-1)
            while selection in voted:
                selection = randint(0,n_candidates-1)
            voted.append(selection)
        ballots.append(deepcopy(voted))
    return ballots

def tally_votes(ballots, n_candidates, n_winners):
    print('Tallying votes...')
    position_votes = []
    for candidate in tqdm(range(n_candidates)):
        position_votes.append([0])
        for position in range(n_candidates):
            position_votes[candidate].append(0)
            pos_count = 0
            x_ballots = [b for b in ballots if position < len(b)]
            for b in x_ballots:
                if b[position] == candidate:
                    pos_count += 1
            position_votes[candidate][position] = pos_count
    #popularity contest tally rounds
    elected = []
    for threshold in range(95,50,-5):
        thresh_pct = threshold / 100.0
        needed = round(len(ballots) * thresh_pct)
        for position in tqdm(range(n_candidates)):
            if len(elected) == n_winners:
                continue
            could_wins = []
            for candidate in range(n_candidates):
                active_votes = 0
                for level in range(position+1):
                    active_votes += position_votes[candidate][level]
                if active_votes >= needed:
                    could_wins.append((candidate, active_votes))
            winners = sorted(could_wins, key=lambda x: x[1], reverse=True)
            for winner in winners:
                if len(elected) == n_winners:
                    break
                if winner[0] not in elected:
                    print(f'{winner[0]} elected in popcon {threshold}%, {position}')
                    elected.append(winner[0])

    #borda rounds
    if len(elected) < n_winners:
        borda_points = [0] * n_candidates
        for i,pts_per_vote in enumerate(range(n_candidates+1,1,-1)):
            for candidate in range(n_candidates):
                borda_points[candidate] += (pts_per_vote *
                            position_votes[candidate][i])
        bwinners = sorted(range(n_candidates), key=lambda x: borda_points[x],
                          reverse=True)
        for bwinner in bwinners:
            if len(elected) == n_winners:
                break
            if bwinner not in elected:
                print(f'{bwinner} elected in borda w {borda_points[bwinner]}')
                elected.append(bwinner)
    return elected

def results(elected, ballots, n_candidates):
    current_ballot = []
    ballot_types = []
    for ballot in ballots:
        if ballot == current_ballot:
            n_this_ballot += 1
        else:
            if current_ballot:
                ballot_types.append([n_this_ballot,current_ballot])
            current_ballot = ballot
            n_this_ballot = 1
    names = [fake.name() for x in range(n_candidates)]
    for bt in ballot_types:
        if bt[0] < 3:
            continue
        print(f'{bt[0]} ballots like this:')
        for nm in bt[1]:
            print(f'\t{names[nm]}')
        print()
    print('and others\n\n')
    for i, name in enumerate(names):
        print(i,name)
    print('The following have been elected in this order:')
    for e in elected:
        print(f'\t{names[e]}')

blocs = gen_blocs(n_blocs, n_candidates)
for b in blocs:
    print(b)
ballots = decide_voters(blocs, n_candidates, n_ballots)
ballots = [b for b in sorted(ballots) if b]
elected = tally_votes(ballots, n_candidates, n_winners)
results(elected, ballots, n_candidates)

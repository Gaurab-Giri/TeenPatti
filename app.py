import streamlit as st
from game_engine import Card, RANKS, SUITS, CATEGORY_NAMES, evaluate_hand, estimate_win_rate, deal_hands

st.set_page_config(page_title='Teen Patti AI Lab', page_icon='🃏', layout='centered')
st.title('🃏 Teen Patti AI Lab')
st.caption('Version 1 — virtual-chip simulator and card probability lab')

with st.sidebar:
    st.header('Table setup')
    players = st.slider('Players', 2, 10, 5)
    boot = st.selectbox('Boot (virtual $)', [0.25, 0.5, 1.0, 2.0, 5.0], index=2)
    bankroll = st.number_input('Starting virtual bankroll ($)', min_value=0.0, value=100.0, step=10.0)
    multiplier = st.selectbox('Seen-to-blind stake multiplier', [1, 2, 4], index=1)
    st.metric('Starting pot', f'${players * boot:.2f}')
    st.metric('Balance after boot', f'${max(0, bankroll - boot):.2f}')
    st.caption('Custom shows, Salami, Vyakso and betting history are coming in later versions.')

st.subheader('Explore a three-card hand')
rank_names = {r: ('10' if r == 'T' else r) for r in RANKS}
suit_names = {'C':'♣ Clubs','D':'♦ Diamonds','H':'♥ Hearts','S':'♠ Spades'}
cols = st.columns(3)
cards = []
for i, col in enumerate(cols):
    with col:
        rank = st.selectbox(f'Card {i + 1} rank', list(RANKS), index=[12, 11, 10][i], format_func=lambda x: rank_names[x], key=f'r{i}')
        suit = st.selectbox(f'Card {i + 1} suit', list(SUITS), index=i, format_func=lambda x: suit_names[x], key=f's{i}')
        cards.append(Card(rank, suit))

if len(set(cards)) < 3:
    st.error('Please select three different cards.')
else:
    score = evaluate_hand(cards)
    st.success(f'Your hand: {CATEGORY_NAMES[score[0]]} — {", ".join(map(str, cards))}')
    trials = st.slider('Monte Carlo trials', 1000, 20000, 5000, step=1000)
    if st.button('Estimate showdown probability', type='primary'):
        with st.spinner('Simulating random opponent hands...'):
            rate = estimate_win_rate(cards, opponents=players - 1, trials=trials)
        st.metric('Estimated share of showdown wins', f'{rate:.1%}')
        st.caption('Random opponents only; tied winning hands split credit. This is not a prediction of actual opponents or a recommendation to wager.')

st.divider()
st.subheader('Generate a practice deal')
if st.button('Deal virtual hands'):
    st.session_state.deal = deal_hands(players)
if 'deal' in st.session_state:
    if len(st.session_state.deal) != players:
        st.info('Player count changed. Deal again to see the new table.')
    else:
        hands = st.session_state.deal
        scores = [evaluate_hand(hand) for hand in hands]
        top = max(scores)
        for i, (hand, score) in enumerate(zip(hands, scores), start=1):
            st.write(f'Player {i}: {" ".join(map(str, hand))} — {CATEGORY_NAMES[score[0]]}')
        winners = [str(i + 1) for i, score in enumerate(scores) if score == top]
        st.info('Winning player(s): ' + ', '.join(winners))

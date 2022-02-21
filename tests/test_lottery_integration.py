from brownie import network
import pytest
import time
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    fund_with_link,
    get_contract,
)
from scripts.deploy import deploy_lottery


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrage
    account = get_account()
    lottery = deploy_lottery()
    # Act
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 1000})
    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 2000})
    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 3000})
    fund_with_link(lottery.address)
    tx = lottery.endLottery({"from": account})
    time.sleep(60)
    # Assert
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0

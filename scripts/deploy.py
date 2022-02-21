from brownie import accounts, config, network, Lottery
from scripts.helpful_scripts import get_account, get_contract, fund_with_link
import time


def deploy_lottery():
    account = get_account()
    feeToPay = config["networks"][network.show_active()]["fee"]
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        feeToPay,
        config["networks"][network.show_active()]["keyHash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed lottery!")
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("The lottery is started!")

def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    entrance_fee = lottery.getEntranceFee() + 100000000
    entering_tx = lottery.enter({"from": account, "value": entrance_fee})
    entering_tx.wait(1)
    print("You entered the lottery!")

def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_tx = lottery.endLottery({"from": account})
    ending_tx.wait(1)
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the new winner!")

def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()

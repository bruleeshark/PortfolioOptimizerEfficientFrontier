# PortfolioOptimizerEfficientFrontier
Calculates the efficient frontier for a 3 asset portfolio and distributes them accordingly to user's specified risk tolerance and expected returns.

# using Poetry package manager
* Install Poetry by following the instructions on the official Poetry website: https://python-poetry.org/docs/#installation
* Clone the project repository to your local machine using the following command:
```
git clone https://github.com/bruleeshark/PortfolioOptimizerEfficientFrontier
```
Replace your_username and your_project with your own information.

* Navigate to the project directory:
```
cd your_project
```

* Install the project dependencies using Poetry:
```
poetry install
```

* Create a .env file in the project root directory and add your private key variable as follows:
```
PRIVATE_KEY=your_private_key
```
Replace your_private_key with your own private key.

* To run the backtest process, run the following command:
```
poetry run python main.py backtest start_date end_date initial_balance fee slippage
```
Replace start_date, end_date, initial_balance, fee, and slippage with the desired parameter inputs.

* If the backtest is satisfactory, to activate and run the bot, run the following command:
```
poetry run python main.py activate
```

# using Miniconda Package Manager:
* Install Miniconda by following the instructions on the official Miniconda website: https://docs.conda.io/en/latest/miniconda.html#installing

* Clone the project repository to your local machine using the following command:
```
git clone https://github.com/bruleeshark/PortfolioOptimizerEfficientFrontier
```
Replace your_username and your_project with your own information.

* Navigate to the project directory:
```
cd your_project
```

* Create a new conda environment with the necessary dependencies by running the following command:
```
conda env create -f environment.yml
```

* Activate the newly created environment:
```
conda activate myenv
```

* Create a .env file in the project root directory and add your private key variable as follows:
```
PRIVATE_KEY=your_private_key
```
Replace your_private_key with your own private key.

* To run the backtest process, run the following command:
```
python main.py backtest start_date end_date initial_balance fee slippage
```
Replace start_date, end_date, initial_balance, fee, and slippage with the desired parameter inputs.

* If the backtest is satisfactory, to activate and run the bot, run the following command:
```
python main.py activate
```

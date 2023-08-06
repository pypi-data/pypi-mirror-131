"""This module do web crawler of banco do brasil."""
__version__ = "0.1.6"

import socket
import time
from datetime import datetime
from random import randrange
from jsmin import jsmin
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

now = datetime.now()

minified = jsmin("""
window.pybancodobrasil = {
    clearStr: (str) => {
        return str.replace(/(\\r\\n|\\n|\\r|\\t)/gm, "").trim()
    },
    table2Json: (table) => {
        var data = [];
        for (var i = 0; i < table.rows.length; i++) {
            var tableRow = table.rows[i];
            var columns = tableRow.querySelectorAll('td')
            var _columns = []
            for (var column of columns){
                if (column.childElementCount==0){
                    _columns.push([window.pybancodobrasil.clearStr(column.innerText)])
                } else {
                    __column = []
                    for (var child of column.children){
                        __column.push(window.pybancodobrasil.clearStr(child.innerText))
                    }
                    _columns.push(__column)
                }
            }
            data.push(_columns)
        }
        return data;
    },
    extratos: {
        counter: 0,
        results: [],
        methods: {
            goto: () => {
                document.querySelector('[codigo="32456"]').click()
            },
            get: (month, year) => {
                window.pybancodobrasil.extratos.counter++;
                $.ajaxApf({
                    atualizaContadorSessao: true,
                    cache: false,
                    funcaoSucesso: (data) => {
                        try {
                            if (data) {
                                const table = $(data).find('table#tabelaExtrato')[0]
                                if (table)
                                    window.pybancodobrasil.extratos.results = [...window.pybancodobrasil.extratos.results, ...window.pybancodobrasil.table2Json(table)];
                            }
                        } catch (error) {
                        }
                        window.pybancodobrasil.extratos.counter--;
                    },
                    funcaoErro: () => {
                        window.pybancodobrasil.extratos.counter--;
                    },
                    parametros: {
                        ambienteLayout: "internoTransacao",
                        confirma: "sim",
                        periodo: `00${month.padStart(2, '0')}${year}`,
                        tipoConta: "",
                        novoLayout: "sim"
                    },
                    simbolo: "30151696898430647187469639762490",
                    tiporetorno: "html",
                    type: "post",
                    url: "/aapf/extrato/009-00-N.jsp"
                })
            }
        }
    },
    faturas: {
        cartoes: {},
        done: false,
        methods: {
            goto: () => {
                document.querySelector('[codigo="32715"]').click()
            },
            cartoes: () => {
                return document.querySelector('#carousel-cartoes').childElementCount;
            },
            faturas: () => {
                return document.querySelectorAll('[indicetabs]').length;
            },
            buscaFaturas: (indice) => {
                var url = "/aapf/cartao/v119-01e2.jsp?indice=" + indice + "&pagina=json";
                var req = configura();
                req.open("GET", url, true);
                req.onreadystatechange = function () {
                    if (req.readyState == 4) {
                        let len = $(req.responseText).find('li').size();
                        window.pybancodobrasil.faturas.methods.buscaExtrato(indice, 0, len, () => {
                            if ((indice + 1) < window.pybancodobrasil.faturas.methods.cartoes()) {
                                window.pybancodobrasil.faturas.methods.buscaFaturas(indice + 1)
                            } else {
                                window.pybancodobrasil.faturas.done = true
                            }
                        })

                    }
                };
                req.send(null);
            },
            buscaExtrato: (_, ind, len, fnEnd) => {
                var indice = ind;
                try {
                    var url = "/aapf/cartao/v119-01e3.jsp?indice=" + indice + "&pagina=normal";
                    var req = configura();
                    req.open("GET", url, true);
                    req.onreadystatechange = function () {
                        if (req.readyState == 4) {
                            var cardInfo = $(req.responseText).find('.textoIdCartao').toArray().map(el => el.innerHTML)
                            var cardNumber = cardInfo[1]
                            if (cardNumber) {
                                if (!window.pybancodobrasil.faturas.cartoes[cardNumber]) {
                                    window.pybancodobrasil.faturas.cartoes[cardNumber] = {}
                                }
                                var vencimento = 'next'
                                try {
                                    vencimento = [...$(req.responseText).find('.vencimentoFatura')[0].childNodes].filter(item => item.nodeName == '#text').map(item => item.textContent).join(' ').trim()
                                } catch (e) { }
                                if (!window.pybancodobrasil.faturas.cartoes[cardNumber][vencimento]) {
                                    window.pybancodobrasil.faturas.cartoes[cardNumber][vencimento] = []
                                }
                                var tables = $(req.responseText).find('table table table').toArray()
                                for (table of tables) {
                                    window.pybancodobrasil.faturas.cartoes[cardNumber][vencimento].push(window.pybancodobrasil.table2Json(table))
                                }
                            }
                            if ((ind + 1) < len) {
                                window.pybancodobrasil.faturas.methods.buscaExtrato(cardNumber, ind + 1, len, fnEnd);
                            } else {
                                fnEnd();
                            }
                        }
                    };
                    req.send(null);
                } catch (e) {
                }
            },
            last: {

            }
        }
    }
}
""")

_default_timeout = 10


def __login(driver, agencia, conta, senha):
    global _default_timeout
    driver.get("https://www2.bancobrasil.com.br/aapf/login.html?1624286762470#/acesso-aapf-agencia-conta-1")
    time.sleep(1)
    WebDriverWait(driver, _default_timeout).until(
        expected_conditions.visibility_of_element_located((By.ID, "dependenciaOrigem")))
    driver.find_element(By.ID, "dependenciaOrigem").send_keys(agencia)
    time.sleep(1)
    WebDriverWait(driver, _default_timeout).until(
        expected_conditions.visibility_of_element_located((By.ID, "numeroContratoOrigem")))
    driver.find_element(By.ID, "numeroContratoOrigem").send_keys(conta)
    time.sleep(1)
    driver.find_element(By.ID, "botaoEnviar").click()
    WebDriverWait(driver, _default_timeout).until(
        expected_conditions.visibility_of_element_located((By.ID, "senhaConta")))
    driver.find_element(By.ID, "senhaConta").send_keys(senha)
    try:
        driver.find_element(By.ID, "botaoEnviar").click()
    except Exception as err_button_sent:
        print('Possible not an error - button sent', __login.__name__, err_button_sent)
    time.sleep(3)
    WebDriverWait(driver, _default_timeout).until(
        expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".menu-completo > .menu-itens")))


def __extratos(driver, init_year=1993):
    global _default_timeout
    try:
        time.sleep(1)
        driver.execute_script(minified)
        driver.execute_script("window.pybancodobrasil.extratos.methods.goto()")
        time.sleep(1)
        for year in range(init_year, now.year + 1):
            for month in range(1, 13):
                if year == now.year and month > now.month:
                    break
                driver.execute_script(
                    'window.pybancodobrasil.extratos.methods.get(\'' + str(month) + '\', \'' + str(year) + '\')')
        counter = 1
        while counter > 0:
            counter = driver.execute_script('return window.pybancodobrasil.extratos.counter')
            time.sleep(0.3)
        time.sleep(1)
        return driver.execute_script('return window.pybancodobrasil.extratos.results')
    except Exception as error:
        print('Error', __extratos.__name__, str(error))
    return []


def __faturas(driver):
    global _default_timeout
    try:
        driver.execute_script(minified)
        driver.execute_script("window.pybancodobrasil.faturas.methods.goto()")
        time.sleep(1)
        driver.execute_script("window.pybancodobrasil.faturas.methods.buscaFaturas(0)")
        done = False
        while not done:
            done = driver.execute_script('return window.pybancodobrasil.faturas.done')
        time.sleep(1)
        return driver.execute_script('return window.pybancodobrasil.faturas.cartoes')
    except Exception as error:
        print('Error', __faturas.__name__, str(error))
    return []


def __cdb(driver):
    global _default_timeout
    driver.execute_script(minified)
    try:
        driver.execute_script("document.querySelector(\'[codigo=\"33130\"]\').click()")
        WebDriverWait(driver, _default_timeout).until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "#botaoContinua")))
        driver.find_element(By.ID, "botaoContinua").click()
        WebDriverWait(driver, _default_timeout).until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "#botaoContinua2")))
        driver.find_element(By.ID, "botaoContinua2").click()
        WebDriverWait(driver, _default_timeout).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, ".transacao-corpo  table:nth-child(6)")))
        lines = driver.find_element(By.CSS_SELECTOR,
                                    ".transacao-corpo  table:nth-child(6)").find_elements_by_css_selector('tr')
        for line in lines:
            if "Saldo liquido projetado" in line.get_attribute('innerText').replace('\xa0', ' '):
                non_blank_items = list(
                    filter(lambda s: s != "", line.get_attribute('innerText').replace('\xa0', ' ').split(' ')))
                replaced_items = list(
                    map(lambda s: s.replace('\n', '').replace('\t', '').replace('.', '').replace(',', '.'),
                        non_blank_items))
                return float(replaced_items[len(replaced_items) - 1])
    except Exception as error:
        print('Error', __cdb.__name__, str(error))
    return None


def _is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def get_free_port():
    port = randrange(1058, 65535)
    while _is_port_in_use(port):
        port = randrange(1058, 65535)
    return port


def get_driver(headless=True, driver='chrome'):
    if driver == 'firefox':
        options = webdriver.FirefoxOptions()
        options.headless = headless
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
        driver.implicitly_wait(10)
        return driver
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options,
                              port=get_free_port())
    driver.implicitly_wait(10)
    return driver


def get(agencia, conta, senha, init_year=1993, headless=True, default_timeout=10, driver='chrome'):
    global _default_timeout
    _default_timeout = default_timeout
    driver = get_driver(headless, driver)
    try:
        __login(driver, agencia, conta, senha)
    except Exception as ex:
        print('Error login', ex)
        return None
    try:
        transactions = __extratos(driver, init_year)
    except Exception as ex:
        print('Error transactions', ex)
        transactions = []
    try:
        cards = __faturas(driver)
    except Exception as ex:
        print('Error cards', ex)
        cards = []
    try:
        cdb = __cdb(driver)
    except Exception as ex:
        print('Error cdb', ex)
        cdb = None
    retorno = {
        'transactions': transactions,
        'cards': cards,
        'cdb': cdb
    }
    driver.quit()
    return retorno

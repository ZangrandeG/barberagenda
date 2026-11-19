package br.com.barberagenda.unit;

import static org.assertj.core.api.Assertions.assertThat;

import java.math.BigDecimal;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.params.provider.ValueSource;

import br.com.barberagenda.dto.ClienteRequest;
import br.com.barberagenda.dto.ServicoRequest;
import jakarta.validation.ConstraintViolation;
import jakarta.validation.Validation;
import jakarta.validation.Validator;
import jakarta.validation.ValidatorFactory;

/** Validações de entrada (Bean Validation) dos cadastros de cliente e de serviço, sem Spring. */
@DisplayName("Validação de entrada — RN-01, RN-02, RN-03 e RN-09")
class ValidacaoEntradaTest {

    private static final String NOME_60 = "Maria Eduarda Fernandes Albuquerque Cavalcanti Souza Ribeiro";
    private static ValidatorFactory fabrica;
    private static Validator validador;

    @BeforeAll
    static void criarValidador() {
        fabrica = Validation.buildDefaultValidatorFactory();
        validador = fabrica.getValidator();
    }

    @AfterAll
    static void fecharValidador() {
        fabrica.close();
    }

    private static <T> Set<String> camposInvalidos(T objeto) {
        return validador.validate(objeto).stream()
                .map(ConstraintViolation::getPropertyPath)
                .map(Object::toString)
                .collect(Collectors.toSet());
    }

    private static <T> Set<String> mensagens(T objeto) {
        return validador.validate(objeto).stream().map(ConstraintViolation::getMessage).collect(Collectors.toSet());
    }

    // ---------------------------------------------------------------- Cliente

    static Stream<Arguments> limitesValidosDoCliente() {
        return Stream.of(
                Arguments.of("nome com 3 caracteres e telefone com 10 dígitos", "Léa", "1432221100"),
                Arguments.of("nome com 60 caracteres e telefone com 11 dígitos", NOME_60, "14999990000"));
    }

    @ParameterizedTest(name = "{0}")
    @MethodSource("limitesValidosDoCliente")
    @DisplayName("CT-002 / RF-01 — aceita nome e telefone nos limites válidos")
    void deveAceitarNomeETelefoneNosLimitesValidos(String descricao, String nome, String telefone) {
        assertThat(camposInvalidos(new ClienteRequest(nome, telefone, "limite@exemplo.com"))).isEmpty();
    }

    @ParameterizedTest(name = "nome com {0} caracteres")
    @MethodSource("nomesForaDoLimite")
    @DisplayName("CT-003 / RF-01 — recusa nome com 2 e com 61 caracteres")
    void deveRejeitarNomeForaDoLimite(int tamanho, String nome) {
        ClienteRequest dados = new ClienteRequest(nome, "14988776655", "limite@exemplo.com");

        assertThat(nome).hasSize(tamanho);
        assertThat(camposInvalidos(dados)).containsExactly("nome");
        assertThat(mensagens(dados)).containsExactly("O nome deve ter entre 3 e 60 caracteres.");
    }

    static Stream<Arguments> nomesForaDoLimite() {
        return Stream.of(Arguments.of(2, "Al"), Arguments.of(61, NOME_60 + "s"));
    }

    @ParameterizedTest(name = "telefone \"{0}\"")
    @ValueSource(strings = {"149887766", "149887766551", "14-98877-6655"})
    @DisplayName("CT-004 / RF-01 — recusa telefone com 9 ou 12 dígitos ou com caracteres não numéricos")
    void deveRejeitarTelefoneForaDoPadrao(String telefone) {
        ClienteRequest dados = new ClienteRequest("Rodrigo Teste", telefone, "rodrigo@exemplo.com");

        assertThat(camposInvalidos(dados)).containsExactly("telefone");
        assertThat(mensagens(dados))
                .containsExactly("O telefone deve conter somente dígitos, com 10 ou 11 dígitos (incluindo DDD).");
    }

    @ParameterizedTest(name = "e-mail \"{0}\"")
    @ValueSource(strings = {"paula.exemplo.com", "paula@exemplo"})
    @DisplayName("CT-005 / RF-01 — recusa e-mail sem @ ou sem domínio de topo")
    void deveRejeitarEmailEmFormatoInvalido(String email) {
        ClienteRequest dados = new ClienteRequest("Paula Teste", "14988776655", email);

        assertThat(camposInvalidos(dados)).containsExactly("email");
        assertThat(mensagens(dados)).containsExactly("O e-mail informado é inválido.");
    }

    // ---------------------------------------------------------------- Serviço

    static Stream<Arguments> limitesValidosDoServico() {
        return Stream.of(
                Arguments.of(15, new BigDecimal("1.00")),
                Arguments.of(180, new BigDecimal("1000.00")));
    }

    @ParameterizedTest(name = "duração {0} min, preço R$ {1}")
    @MethodSource("limitesValidosDoServico")
    @DisplayName("CT-030 / RF-07 — aceita duração e preço nos limites válidos")
    void deveAceitarServicoNosLimitesValidos(int duracao, BigDecimal preco) {
        assertThat(camposInvalidos(new ServicoRequest("Serviço Limite", duracao, preco, true))).isEmpty();
    }

    @ParameterizedTest(name = "duração {0} min")
    @ValueSource(ints = {14, 20, 195})
    @DisplayName("CT-031 / RF-07 — recusa duração menor que 15, não múltipla de 15 ou maior que 180")
    void deveRejeitarDuracaoForaDosLimites(int duracao) {
        ServicoRequest dados = new ServicoRequest("Serviço Limite", duracao, new BigDecimal("10.00"), true);

        assertThat(camposInvalidos(dados)).containsExactly("duracaoMinutos");
    }

    @ParameterizedTest(name = "preço R$ {0}")
    @ValueSource(strings = {"0.99", "1000.01"})
    @DisplayName("CT-031 / RF-07 — recusa preço abaixo de R$ 1,00 ou acima de R$ 1.000,00")
    void deveRejeitarPrecoForaDosLimites(String preco) {
        ServicoRequest dados = new ServicoRequest("Serviço Limite", 30, new BigDecimal(preco), true);

        assertThat(camposInvalidos(dados)).containsExactly("preco");
    }
}

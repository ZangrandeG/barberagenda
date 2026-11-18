package br.com.barberagenda.seed;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.context.annotation.Profile;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

import br.com.barberagenda.repository.BarbeiroRepository;

/** Carrega a massa fictícia na inicialização (perfis dev e test), somente se o banco estiver vazio. */
@Component
@Profile({"dev", "test"})
@Order(2)
public class InicializadorDadosFicticios implements ApplicationRunner {

    private static final Logger LOG = LoggerFactory.getLogger(InicializadorDadosFicticios.class);

    private final BarbeiroRepository barbeiroRepository;
    private final CargaDadosFicticios carga;

    public InicializadorDadosFicticios(BarbeiroRepository barbeiroRepository, CargaDadosFicticios carga) {
        this.barbeiroRepository = barbeiroRepository;
        this.carga = carga;
    }

    @Override
    public void run(ApplicationArguments args) {
        if (barbeiroRepository.count() == 0) {
            ResumoCarga resumo = carga.carregar();
            LOG.info("Massa de dados fictícios carregada: {}", resumo);
        }
    }
}

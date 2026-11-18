package br.com.barberagenda.service;

import java.util.List;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import br.com.barberagenda.dto.BarbeiroRequest;
import br.com.barberagenda.exception.ConflitoException;
import br.com.barberagenda.exception.RecursoNaoEncontradoException;
import br.com.barberagenda.model.Barbeiro;
import br.com.barberagenda.repository.AgendamentoRepository;
import br.com.barberagenda.repository.BarbeiroRepository;

@Service
public class BarbeiroService {

    private final BarbeiroRepository barbeiroRepository;
    private final AgendamentoRepository agendamentoRepository;

    public BarbeiroService(BarbeiroRepository barbeiroRepository, AgendamentoRepository agendamentoRepository) {
        this.barbeiroRepository = barbeiroRepository;
        this.agendamentoRepository = agendamentoRepository;
    }

    @Transactional(readOnly = true)
    public List<Barbeiro> listarAtivos() {
        return barbeiroRepository.findByAtivoTrueOrderByNomeAsc();
    }

    @Transactional(readOnly = true)
    public List<Barbeiro> listarTodos() {
        return barbeiroRepository.findAllByOrderByNomeAsc();
    }

    @Transactional(readOnly = true)
    public Barbeiro buscar(Long id) {
        return barbeiroRepository.findById(id)
                .orElseThrow(() -> new RecursoNaoEncontradoException("Barbeiro não encontrado."));
    }

    @Transactional
    public Barbeiro cadastrar(BarbeiroRequest dados) {
        return barbeiroRepository.save(new Barbeiro(dados.nome(), dados.ativoOuPadrao()));
    }

    @Transactional
    public Barbeiro atualizar(Long id, BarbeiroRequest dados) {
        Barbeiro barbeiro = buscar(id);
        barbeiro.atualizar(dados.nome(), dados.ativoOuPadrao());
        return barbeiro;
    }

    /** Exclui o barbeiro. Se ele já possui agendamentos, a exclusão é recusada (use a desativação). */
    @Transactional
    public void excluir(Long id) {
        Barbeiro barbeiro = buscar(id);
        if (agendamentoRepository.existsByBarbeiroId(id)) {
            throw new ConflitoException(
                    "O barbeiro possui agendamentos e não pode ser excluído. Desative-o em vez de excluir.");
        }
        barbeiroRepository.delete(barbeiro);
    }
}

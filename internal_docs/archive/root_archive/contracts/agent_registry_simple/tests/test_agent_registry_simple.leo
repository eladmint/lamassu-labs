// The 'test_agent_registry_simple' test program.
import agent_registry_simple.aleo;
program test_agent_registry_simple.aleo {
    @test
    script test_it() {
        let result: u32 = agent_registry_simple.aleo/main(1u32, 2u32);
        assert_eq(result, 3u32);
    }

    @test
    @should_fail
    transition do_nothing() {
        let result: u32 = agent_registry_simple.aleo/main(2u32, 3u32);
        assert_eq(result, 3u32);
    }
}

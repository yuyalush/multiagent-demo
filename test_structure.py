"""
Test script to validate the multi-agent system structure
This tests the code structure without requiring Azure OpenAI credentials
"""
import sys
import inspect


def test_imports():
    """Test that all modules can be imported"""
    try:
        import technical_agent
        import business_agent
        import orchestrator_agent
        import main
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_class_structure():
    """Test that all required classes and methods exist"""
    from technical_agent import TechnicalAgent
    from business_agent import BusinessAgent
    from orchestrator_agent import OrchestratorAgent
    
    errors = []
    
    # Check TechnicalAgent
    if not hasattr(TechnicalAgent, '__init__'):
        errors.append("TechnicalAgent missing __init__")
    if not hasattr(TechnicalAgent, 'process'):
        errors.append("TechnicalAgent missing process method")
    if not hasattr(TechnicalAgent, 'get_system_prompt'):
        errors.append("TechnicalAgent missing get_system_prompt method")
    
    # Check BusinessAgent
    if not hasattr(BusinessAgent, '__init__'):
        errors.append("BusinessAgent missing __init__")
    if not hasattr(BusinessAgent, 'process'):
        errors.append("BusinessAgent missing process method")
    if not hasattr(BusinessAgent, 'get_system_prompt'):
        errors.append("BusinessAgent missing get_system_prompt method")
    
    # Check OrchestratorAgent
    if not hasattr(OrchestratorAgent, '__init__'):
        errors.append("OrchestratorAgent missing __init__")
    if not hasattr(OrchestratorAgent, 'process'):
        errors.append("OrchestratorAgent missing process method")
    if not hasattr(OrchestratorAgent, 'classify_query'):
        errors.append("OrchestratorAgent missing classify_query method")
    if not hasattr(OrchestratorAgent, 'synthesize_responses'):
        errors.append("OrchestratorAgent missing synthesize_responses method")
    
    if errors:
        for error in errors:
            print(f"✗ {error}")
        return False
    
    print("✓ All required classes and methods exist")
    return True


def test_method_signatures():
    """Test that methods have correct signatures"""
    from technical_agent import TechnicalAgent
    from business_agent import BusinessAgent
    from orchestrator_agent import OrchestratorAgent
    
    errors = []
    
    # Check TechnicalAgent.process signature
    sig = inspect.signature(TechnicalAgent.process)
    if 'query' not in sig.parameters:
        errors.append("TechnicalAgent.process missing 'query' parameter")
    
    # Check BusinessAgent.process signature
    sig = inspect.signature(BusinessAgent.process)
    if 'query' not in sig.parameters:
        errors.append("BusinessAgent.process missing 'query' parameter")
    
    # Check OrchestratorAgent.process signature
    sig = inspect.signature(OrchestratorAgent.process)
    if 'query' not in sig.parameters:
        errors.append("OrchestratorAgent.process missing 'query' parameter")
    
    # Check OrchestratorAgent.classify_query signature
    sig = inspect.signature(OrchestratorAgent.classify_query)
    if 'query' not in sig.parameters:
        errors.append("OrchestratorAgent.classify_query missing 'query' parameter")
    
    if errors:
        for error in errors:
            print(f"✗ {error}")
        return False
    
    print("✓ All method signatures are correct")
    return True


def test_agent_attributes():
    """Test that agents have required attributes"""
    from technical_agent import TechnicalAgent
    from business_agent import BusinessAgent
    from orchestrator_agent import OrchestratorAgent
    
    # We can't instantiate without a client, but we can check the class structure
    errors = []
    
    # Check that __init__ methods have the right parameters
    tech_init_sig = inspect.signature(TechnicalAgent.__init__)
    if 'client' not in tech_init_sig.parameters or 'deployment_name' not in tech_init_sig.parameters:
        errors.append("TechnicalAgent.__init__ missing required parameters")
    
    bus_init_sig = inspect.signature(BusinessAgent.__init__)
    if 'client' not in bus_init_sig.parameters or 'deployment_name' not in bus_init_sig.parameters:
        errors.append("BusinessAgent.__init__ missing required parameters")
    
    orch_init_sig = inspect.signature(OrchestratorAgent.__init__)
    if 'client' not in orch_init_sig.parameters or 'deployment_name' not in orch_init_sig.parameters:
        errors.append("OrchestratorAgent.__init__ missing required parameters")
    
    if errors:
        for error in errors:
            print(f"✗ {error}")
        return False
    
    print("✓ All agent initialization parameters are correct")
    return True


def test_main_functions():
    """Test that main.py has required functions"""
    import main
    
    errors = []
    
    if not hasattr(main, 'initialize_client'):
        errors.append("main.py missing initialize_client function")
    if not hasattr(main, 'run_demo'):
        errors.append("main.py missing run_demo function")
    if not hasattr(main, 'print_result'):
        errors.append("main.py missing print_result function")
    
    if errors:
        for error in errors:
            print(f"✗ {error}")
        return False
    
    print("✓ All required functions in main.py exist")
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("Multi-Agent System Structure Tests")
    print("=" * 60)
    print()
    
    tests = [
        ("Module Imports", test_imports),
        ("Class Structure", test_class_structure),
        ("Method Signatures", test_method_signatures),
        ("Agent Attributes", test_agent_attributes),
        ("Main Functions", test_main_functions),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Running: {test_name}")
        result = test_func()
        results.append((test_name, result))
        print()
    
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 60)
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())

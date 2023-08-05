import os
import unittest
import json
import logging
import subprocess
import warnings
from policy_sentry.command.query import query
from policy_sentry.command.write_policy import write_policy
from kinnaird_utils.shell import run_click_command, run_shell_command
from kinnaird_utils.testing_utils import ignore_warnings
from kinnaird_utils.log_formatting import set_stream_logger
logger = logging.getLogger(__name__)
warnings.simplefilter("ignore", ResourceWarning)


class ShellTestCase(unittest.TestCase):

    def test_run_shell_command_wait(self):
        command = "echo 'sup'"
        results = run_shell_command(command=command, timeout=5, shell=False)
        print(results.__dict__)
        self.assertTrue(results.stdout == "sup\n")
        self.assertTrue(results.returncode == 0)

    @ignore_warnings
    def test_run_shell_command_dont_wait(self):
        command = "echo 'sup'"
        # unittest.main(warnings='ignore')
        results = run_shell_command(command=command, timeout=5, shell=False, wait_for_finish=False)
        print(results.__dict__)
        print(results.stdout.__dict__)

    def test_run_click_command(self):
        results = run_click_command(query, args="action-table --service ram")
        print(results.output)
        # Expected results:
        """
ALL ram actions:
ram:AcceptResourceShareInvitation
ram:AssociateResourceShare
ram:AssociateResourceSharePermission
ram:CreateResourceShare
ram:DeleteResourceShare
ram:DisassociateResourceShare
ram:DisassociateResourceSharePermission
ram:EnableSharingWithAwsOrganization
ram:GetPermission
ram:GetResourcePolicies
ram:GetResourceShareAssociations
ram:GetResourceShareInvitations
ram:GetResourceShares
ram:ListPendingInvitationResources
ram:ListPermissions
ram:ListPrincipals
ram:ListResourceSharePermissions
ram:ListResourceTypes
ram:ListResources
ram:PromoteResourceShareCreatedFromPolicy
ram:RejectResourceShareInvitation
ram:TagResource
ram:UntagResource
ram:UpdateResourceShare

        """
        self.assertTrue("ram:GetPermission" in results.output)

    def test_run_click_command_fail(self):
        with self.assertRaises(FileNotFoundError):
            results = run_click_command(write_policy, args="--input-file doesnotexist.yml")
